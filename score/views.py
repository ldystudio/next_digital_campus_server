from django.conf import settings
from pydash import map_, group_by
from rest_framework import generics
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_tracking.mixins import LoggingMixin
from zhipuai import ZhipuAI

from common.cache import CacheFnMixin
from common.pagination import UnlimitedPagination
from common.permissions import (
    IsTeacherOrAdminUser,
    IsOwnerOperation,
    IsStudentOrAdminUser,
    IsStudent,
)
from common.result import Result
from common.utils.decide import is_admin, validation_year
from common.viewsets import ModelViewSetFormatResult, ReadOnlyModelViewSetFormatResult
from .filters import ScoreInformationFilter
from .models import Information
from .serializers import (
    ScoreInformationSerializer,
    ScoreQuerySerializer,
    ScoreDataSerializer,
    ScoreAIAdviseSerializer,
)


class ScoreInformationViewSet(ModelViewSetFormatResult):
    queryset = Information.objects.all().distinct()
    serializer_class = ScoreInformationSerializer
    filterset_class = ScoreInformationFilter
    permission_classes = (IsTeacherOrAdminUser, IsOwnerOperation)
    cache_paths_to_delete = ["score/query/", "score/peacetime/"]

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            if not is_admin(self.request):
                return queryset.filter(course__teacher=self.request.user.teacher)
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
            student=self.request.user.student,
            course__start_date__year=year,
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

    # @cache_response(key_func="list_cache_key_func", timeout=60 * 60 * 10)
    def list(self, request, *args, **kwargs):
        year = validation_year(request.query_params.get("year"))

        queryset = self.get_queryset().filter(
            student=self.request.user.student,
            course__start_date__year=year,
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
                    "content": f"作为一个 AI 学习助手，你的任务是根据学生的成绩提出学业建议，并用markdown格式进行展示，现在这名学生的学习成绩如下：```{serializer.data}```",
                }
            ],
        )

        return Result.OK_200_SUCCESS(data=response.choices[0].message.content)
