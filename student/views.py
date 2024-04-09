from datetime import datetime

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_tracking.mixins import LoggingMixin

from common.permissions import IsOwnerOperation
from common.result import Result
from common.viewsets import ReadWriteModelViewSetFormatResult, ModelViewSetFormatResult
from .filters import (
    StudentInformationFilter,
    StudentEnrollmentFilter,
    StudentAttendanceFilter,
)
from .models import Information, Enrollment, Attendance
from .serializers import (
    StudentInformationSerializer,
    StudentEnrollmentSerializer,
    StudentAttendanceSerializer,
)


# Create your views here.
class StudentInformationViewSet(ReadWriteModelViewSetFormatResult):
    queryset = Information.objects.all()
    serializer_class = StudentInformationSerializer
    filterset_class = StudentInformationFilter
    user_fields = ["real_name", "phone", "email", "avatar"]

    def perform_update(self, serializer):
        self.delete_cache_by_path_prefix(
            path=f"/api/v1/auth/user/{self.request.user.id}"
        )
        super().perform_update(serializer)


class StudentEnrollmentViewSet(ReadWriteModelViewSetFormatResult):
    queryset = Enrollment.objects.all()
    serializer_class = StudentEnrollmentSerializer
    filterset_class = StudentEnrollmentFilter
    user_fields = ["real_name"]

    def perform_update(self, serializer):
        self.delete_cache_by_path_prefix(
            path=f"/api/v1/auth/user/{self.request.user.id}"
        )
        super().perform_update(serializer)


class StudentAttendanceViewSet(ModelViewSetFormatResult):
    queryset = Attendance.objects.all()
    serializer_class = StudentAttendanceSerializer
    filterset_class = StudentAttendanceFilter


class StudentTodayAttendanceGenericsView(LoggingMixin, generics.ListAPIView):
    queryset = Attendance.objects.all().filter(
        date=datetime.today().strftime("%Y-%m-%d")
    )
    serializer_class = StudentAttendanceSerializer
    permission_classes = (IsOwnerOperation,)

    logging_methods = ["GET"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset().filter(user_id=request.user.id)
        )
        serializer = self.get_serializer(self.paginate_queryset(queryset), many=True)
        paginated_response = self.get_paginated_response(serializer.data)
        return Result.OK_200_SUCCESS(data=paginated_response.data)
