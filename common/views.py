from django.conf import settings
from django.core.cache import cache
from django.db.models import Q, Avg
from django.utils import timezone
from rest_framework import generics
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework_tracking.models import APIRequestLog

from common.cache import CacheFnMixin
from common.permissions import IsAdminUser
from common.result import Result
from common.serializer.log import (
    APIRequestLogSerializer,
    APIRequestResponseLogSerializer,
    APIRequestErrorsLogSerializer,
)
from common.utils.decide import is_admin
from common.utils.generate import generate_chart, generate_random_data
from common.viewsets import (
    ReadOnlyModelViewSetFormatResult,
    RetrieveModelViewSetFormatResult,
)
from student.models import Information as Student, Enrollment as StudentEnrollment
from teacher.models import Information as Teacher


class APIRequestLogViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = APIRequestLog.objects.all().order_by("-id")
    serializer_class = APIRequestLogSerializer
    permission_classes = (IsAdminUser,)
    filterset_fields = ("username_persistent",)


class APIRequestLogResponseLogViewSet(RetrieveModelViewSetFormatResult):
    queryset = APIRequestLog.objects.values("id", "response").order_by("-id")
    serializer_class = APIRequestResponseLogSerializer
    permission_classes = (IsAdminUser,)


class APIRequestLogErrorsLogViewSet(RetrieveModelViewSetFormatResult):
    queryset = APIRequestLog.objects.values("id", "errors").order_by("-id")
    serializer_class = APIRequestErrorsLogSerializer
    permission_classes = (IsAdminUser,)


class DashboardChartView(LoggingMixin, CacheFnMixin, generics.ListAPIView):
    logging_methods = ["GET"]

    @cache_response(key_func="list_cache_key_func")
    def list(self, request, *args, **kwargs):
        chart1 = generate_chart(
            "学生签到率统计", "Student attendance statistics", "签到人数", (100, 300), 7
        )
        chart2 = generate_chart(
            "活动参与度统计", "Activity participation statistics", "参与人数", (10, 100), 7
        )

        chart3 = {}
        if is_admin(request):
            current_year = timezone.now().year
            grade_names = ["大一", "大二", "大三", "大四"]
            chart3 = {
                "title": "各年级人数比例",
                "describe": "The proportion of students",
                "data": [
                    {
                        "name": grade_names[i],
                        "value": StudentEnrollment.objects.filter(
                            date_of_admission__year=current_year - i
                        ).count(),
                    }
                    for i in range(len(grade_names))
                ],
            }

        large_chart = {
            "chart1": {"title": "电脑", "data": generate_random_data(14)},
            "chart2": {"title": "手机", "data": generate_random_data(14)},
            "chart3": {
                "series1": {"name": "学生", "data": generate_random_data(10, 2, 7)},
                "series2": {"name": "教师", "data": generate_random_data(10, 2, 8)},
            },
        }
        return Result.OK_200_SUCCESS(
            data={
                "chart1": chart1,
                "chart2": chart2,
                "chart3": chart3,
                "large_chart": large_chart,
            }
        )


class DashboardAnalyticsView(LoggingMixin, CacheFnMixin, generics.ListAPIView):
    logging_methods = ["GET"]

    @cache_response(key_func="list_cache_key_func", timeout=10)
    def list(self, request, *args, **kwargs):
        summary_card = {}
        if is_admin(request):
            qs_student = Student.objects.all()
            qs_teacher = Teacher.objects.all()
            summary_card["first"] = {
                "title": "注册学生人数",
                "describe": (total_student := qs_student.count()),
                "icon": "solar:users-group-two-rounded-bold-duotone",
                "numValue": qs_student.filter(
                    date_joined__contains=timezone.now().date()
                ).count()
                // total_student,
            }
            summary_card["second"] = {
                "title": "注册教师人数",
                "describe": (total_teacher := qs_teacher.count()),
                "icon": "solar:users-group-rounded-bold",
                "numValue": qs_teacher.filter(
                    date_joined__contains=timezone.now().date()
                ).count()
                // total_teacher,
            }
            summary_card["third"] = {
                "title": "在线用户人数",
                "describe": len(cache.keys("access_user_id=*", version="AccessList")),
                "icon": "solar:user-check-bold-duotone",
            }
            summary_card["fourth"] = {
                "title": "平均响应时间",
                "describe": "{:.2f}".format(
                    APIRequestLog.objects.filter(
                        ~Q(
                            path__in=[
                                f"/{settings.API_VERSION}auth/email_captcha/",
                                f"/{settings.API_VERSION}score/ai-advise/",
                                f"/{settings.API_VERSION}score/statistics/",
                                f"/{settings.API_VERSION}dashboard/analytics/",
                                f"/{settings.API_VERSION}auth/login/",
                            ]
                        ),
                        errors__isnull=True,
                        method="GET",
                    )
                    .order_by("-pk")[:50]
                    .aggregate(Avg("response_ms"))
                    .get("response_ms__avg")
                )
                + " ms",
                "icon": "solar:user-check-bold-duotone",
            }
        return Result.OK_200_SUCCESS(data=summary_card)
