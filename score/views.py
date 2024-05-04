from collections import Counter

import jieba
from django.conf import settings
from django.db.models import Max, Avg, Min, Q
from django.utils import timezone
from pydash import group_by, map_, map_values
from rest_framework import generics
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_tracking.mixins import LoggingMixin
from zhipuai import ZhipuAI

from classes.models import Information as Classes
from common.cache import CacheFnMixin
from common.pagination import UnlimitedPagination
from common.permissions import (
    IsTeacherOrAdminUser,
    IsOwnerOperation,
    IsStudentOrAdminUser,
    IsStudent,
)
from common.result import Result
from common.utils.decide import is_admin, validation_year, is_teacher, is_student
from common.viewsets import ModelViewSetFormatResult, ReadOnlyModelViewSetFormatResult
from .filters import ScoreInformationFilter
from .models import Information
from .serializers import *


class ScoreInformationViewSet(ModelViewSetFormatResult):
    queryset = Information.objects.all().distinct()
    serializer_class = ScoreInformationSerializer
    filterset_class = ScoreInformationFilter
    permission_classes = (IsTeacherOrAdminUser, IsOwnerOperation)
    cache_paths_to_delete = ["score/"]

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            if not is_admin(self.request):
                return queryset.filter(
                    Q(course__teacher=(teacher := self.request.user.teacher))
                    | Q(course__classes__in=teacher.classes.all())
                )
            return queryset


class ScoreQueryViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = Information.objects.all().distinct()
    serializer_class = ScoreQuerySerializer
    filterset_class = ScoreInformationFilter
    permission_classes = (IsStudentOrAdminUser, IsOwnerOperation)
    pagination_class = UnlimitedPagination

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            if not is_admin(self.request):
                return queryset.filter(student=self.request.user.student)
        return queryset


class PeacetimeScoreListView(LoggingMixin, CacheFnMixin, generics.ListAPIView):
    queryset = Information.objects.filter(exam_type=1).order_by("exam_date")
    serializer_class = ScoreDataSerializer
    permission_classes = (IsStudent,)
    logging_methods = ["GET"]

    @cache_response(key_func="list_cache_key_func")
    def list(self, request, *args, **kwargs):
        year = validation_year(request.query_params.get("year"))

        queryset = self.get_queryset().filter(
            student=self.request.user.student, course__start_date__year=year
        )
        serializer = self.get_serializer(queryset, many=True)

        formatted_data = {
            key.split("-")[1]: map_(
                value, lambda item: [item["exam_date"], item["exam_score"]]
            )
            for key, value in group_by(serializer.data, lambda x: x["course"]).items()
        }

        return Result.OK_200_SUCCESS(data=formatted_data)


class ScoreAIAdviseView(LoggingMixin, CacheFnMixin, generics.ListAPIView):
    queryset = Information.objects.all().order_by("exam_date")
    serializer_class = ScoreAIAdviseSerializer
    permission_classes = (IsStudent,)
    logging_methods = ["GET"]

    @cache_response(key_func="list_cache_key_func", timeout=60 * 60 * 10)
    def list(self, request, *args, **kwargs):
        year = validation_year(request.query_params.get("year"))

        queryset = self.get_queryset().filter(
            student=self.request.user.student, course__start_date__year=year
        )
        serializer = self.get_serializer(queryset, many=True)

        if not serializer.data:
            return Result.OK_200_SUCCESS(data="暂无建议，请继续努力！")

        client = ZhipuAI(api_key=settings.ZHI_PU_API_KEY)
        response = client.chat.completions.create(
            model="glm-3-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"""作为一个 AI 学习助手，你的任务是根据学生的成绩提出学业建议，并用<p>、<ol>、<li>、<strong>、<em>等标签包裹建议内容，
                以便更好的呈现给学生。现在这名学生的学习成绩如下：```{serializer.data}```""",
                }
            ],
        )

        return Result.OK_200_SUCCESS(data=response.choices[0].message.content)


class ScoreStatisticsView(LoggingMixin, CacheFnMixin, generics.ListAPIView):
    queryset = Information.objects.all().distinct()
    logging_methods = ["GET"]

    @cache_response(key_func="list_cache_key_func")
    def list(self, request, *args, **kwargs):
        if is_admin(request):
            return Result.OK_200_SUCCESS(data=None)
        elif is_teacher(request):
            queryset = self.get_queryset().filter(
                Q(course__classes__in=request.user.teacher.classes.all())
                | Q(course__teacher=request.user.teacher)
            )
        else:
            queryset = self.get_queryset().filter(student=request.user.student)
        # ================================================
        max_score = queryset.aggregate(Max("exam_score"))["exam_score__max"]
        avg_score = queryset.aggregate(Avg("exam_score"))["exam_score__avg"]
        min_score = queryset.aggregate(Min("exam_score"))["exam_score__min"]
        # ================================================
        excellent = queryset.filter(exam_score__gte=90).count()
        good = queryset.filter(exam_score__gte=80, exam_score__lt=90).count()
        pass_ = queryset.filter(exam_score__gte=60, exam_score__lt=80).count()
        poor = queryset.filter(exam_score__lt=60).count()

        pie_chart = [
            {"name": "优秀", "value": excellent},
            {"name": "良好", "value": good},
            {"name": "及格", "value": pass_},
            {"name": "不及格", "value": poor},
        ]
        # ================================================
        if is_student(request):
            years = list(
                *StudentEnrollment.objects.filter(user=request.user).values_list(
                    "date_of_admission__year", "date_of_graduation__year"
                )
            )
        else:
            years = [(now := timezone.now().year) - 4, now]
        years_range = list(range(years[0], years[-1] + 1))

        qs = queryset.filter(course__start_date__year__in=years_range, exam_type=3)
        names = set(qs.values_list("course__course_name", flat=True))

        res = {}
        for name in names:
            _data = []
            for year in years_range:
                score = qs.filter(
                    course__start_date__year=year, course__course_name=name
                ).values_list("exam_score", flat=True)
                if is_student(request):
                    _data.append(score.first() if len(score) > 0 else None)
                else:
                    _data.append(
                        round(sum(score) / len(score), 2) if len(score) > 0 else None
                    )
            res[name] = _data

        bar_chart = {"years": years_range, "names": names, "values": res}
        # ================================================
        if is_student(request):
            course_names = Course.objects.filter(
                Q(classes=self.request.user.student_enrollment.classes)
                | Q(student=self.request.user.student)
            ).values_list("course_name", flat=True)
        else:
            course_names = Course.objects.filter(
                Q(classes__in=self.request.user.teacher.classes.all())
                | Q(teacher=request.user.teacher)
            ).values_list("course_name", flat=True)

        word_count = Counter()
        for word in course_names:
            seg_list = jieba.cut(word)
            word_count.update(seg_list)

        word_cloud = [
            {"name": k, "value": v} for k, v in word_count.items() if len(k) > 1
        ]
        # ================================================
        # 查找本学生在期末考试的本班级成绩排名
        if is_student(request):
            scores = queryset.filter(exam_type=3).order_by("-exam_score")
            best_course = scores.first().course.course_name
            worst_course = scores.last().course.course_name
            class_scores = Information.objects.filter(
                exam_type=3,
                course__classes=(
                    student_classes := self.request.user.student_enrollment.classes
                ),
            ).values("student__id", "exam_score")
            total_scores = map_values(
                group_by(class_scores, "student__id"),
                lambda x: sum(item["exam_score"] for item in x),
            )
            sorted_scores = sorted(
                total_scores.items(), key=lambda x: x[1], reverse=True
            )
            rank = (
                sorted_scores.index(
                    (student_id := request.user.student.id, total_scores[student_id])
                )
                + 1
            )
            total_students = (
                Classes.objects.filter(id=student_classes.id)
                .values_list("student_enrollment", flat=True)
                .count()
            )
            class_rank = f"{rank} / {total_students}"
        else:
            class_scores = Information.objects.filter(
                exam_type=3,
                course__classes__in=(self.request.user.teacher.classes.all()),
            ).values("course__course_name", "exam_score")
            total_scores = map_values(
                group_by(class_scores, "course__course_name"),
                lambda x: sum(item["exam_score"] for item in x),
            )
            sorted_scores = sorted(
                total_scores.items(), key=lambda x: x[1], reverse=True
            )
            best_course = sorted_scores[0][0]
            worst_course = sorted_scores[-1][0]
            class_rank = "暂无数据"

        return Result.OK_200_SUCCESS(
            data={
                "max": max_score,
                "avg": avg_score,
                "min": min_score,
                "best_course": best_course,
                "worst_course": worst_course,
                "class_rank": class_rank,
                "pie_chart": pie_chart,
                "bar_chart": bar_chart,
                "word_cloud": word_cloud,
            }
        )
