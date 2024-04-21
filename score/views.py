from pydash import map_, group_by, order_by
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_tracking.mixins import LoggingMixin

from common.cache import CacheFnMixin
from common.permissions import (
    IsTeacherOrAdminUser,
    IsOwnerOperation,
    IsStudentOrAdminUser,
    IsStudent,
)
from common.result import Result
from common.utils.decide import is_admin
from common.viewsets import ModelViewSetFormatResult, ReadOnlyModelViewSetFormatResult
from .filters import ScoreInformationFilter
from .models import Information
from .serializers import (
    ScoreInformationSerializer,
    ScoreQuerySerializer,
    ScoreDataSerializer,
)


class ScoreInformationViewSet(ModelViewSetFormatResult):
    queryset = Information.objects.all().distinct()
    serializer_class = ScoreInformationSerializer
    filterset_class = ScoreInformationFilter
    permission_classes = (IsTeacherOrAdminUser, IsOwnerOperation)

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

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            if not is_admin(self.request):
                return queryset.filter(student=self.request.user.student)
        return queryset


class PeacetimeScoreListView(LoggingMixin, CacheFnMixin, generics.ListAPIView):
    queryset = Information.objects.filter(exam_type=1)
    serializer_class = ScoreDataSerializer
    permission_classes = (IsStudent,)
    logging_methods = ["GET"]

    # @cache_response(key_func="list_cache_key_func")
    def list(self, request, *args, **kwargs):
        year = request.query_params.get("year")
        if year and not year.isdigit() or int(year) < 2000 or int(year) > 9999:
            raise ValidationError("年份格式不正确。")

        queryset = self.get_queryset().filter(
            student=self.request.user.student,
            course__start_date__year=year,
        )
        serializer = self.get_serializer(queryset, many=True)

        group_data = group_by(serializer.data, lambda x: x["course"])
        sorted_data = {
            key: order_by(value, ["exam_date"]) for key, value in group_data.items()
        }
        formatted_data = {
            key.split("-")[1]: map_(
                value, lambda item: [item["exam_date"], item["exam_score"]]
            )
            for key, value in sorted_data.items()
        }

        return Result.OK_200_SUCCESS(data=formatted_data)
