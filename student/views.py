from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from common.permissions import IsOwnerOperation, IsAdminUser
from common.result import Result
from common.viewsets import ReadWriteModelViewSetFormatResult, ModelViewSetFormatResult
from iam.models import User
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
    permission_classes = (IsOwnerOperation,)
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend)
    filterset_class = StudentInformationFilter

    def get_permissions(self):
        # 仅对“list”操作应用IsAdminUser权限
        return (IsAdminUser(),) if self.action == "list" else super().get_permissions()

    def split_data(self, request_data):
        user_data = {}
        information_data = {}
        for key, value in request_data.items():
            if key in ["real_name", "phone", "email", "avatar"]:
                user_data[key] = value
            elif key in self.serializer_class().get_fields():
                information_data[key] = value
        return user_data, information_data

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = User.objects.get(id=instance.user_id)
        except (User.DoesNotExist, Information.DoesNotExist):
            return Result.FAIL_404_NOT_FOUND(msg="用户或信息不存在")

        user_data, information_data = self.split_data(request.data)

        # 判断并更新User表
        if user_data:
            for attr, val in user_data.items():
                setattr(user, attr, val)
            user.save()

        # 判断并更新Information表
        if information_data:
            for attr, val in information_data.items():
                setattr(instance, attr, val)
            instance.save()

        serializer = self.get_serializer(instance)
        return Result.OK_202_ACCEPTED(data=serializer.data)


class StudentEnrollmentViewSet(ReadWriteModelViewSetFormatResult):
    queryset = Enrollment.objects.all()
    serializer_class = StudentEnrollmentSerializer
    permission_classes = (IsOwnerOperation,)
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend)
    filterset_class = StudentEnrollmentFilter

    def get_permissions(self):
        # 仅对“list”操作应用IsAdminUser权限
        return (IsAdminUser(),) if self.action == "list" else super().get_permissions()

    def split_data(self, request_data):
        user_data = {}
        enrollment_data = {}
        for key, value in request_data.items():
            if key in ["real_name"]:
                user_data[key] = value
            elif key in self.serializer_class().get_fields():
                enrollment_data[key] = value
        return user_data, enrollment_data

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = User.objects.get(id=instance.user_id)
        except (User.DoesNotExist, Enrollment.DoesNotExist):
            return Result.FAIL_404_NOT_FOUND(msg="用户或信息不存在")

        user_data, enrollment_data = self.split_data(request.data)

        # 判断并更新User表
        if user_data:
            for attr, val in user_data.items():
                setattr(user, attr, val)
            user.save()

        # 判断并更新Information表
        if enrollment_data:
            for attr, val in enrollment_data.items():
                setattr(instance, attr, val)
            instance.save()

        serializer = self.get_serializer(instance)
        return Result.OK_202_ACCEPTED(data=serializer.data)


class StudentAttendanceViewSet(ModelViewSetFormatResult):
    queryset = Attendance.objects.all()
    serializer_class = StudentAttendanceSerializer
    permission_classes = (IsOwnerOperation,)
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend)
    filterset_class = StudentAttendanceFilter

    # def get_permissions(self):
    #     # 仅对“list”操作应用IsAdminUser权限
    #     return (IsAdminUser(),) if self.action == "list" else super().get_permissions()

    def split_data(self, request_data):
        user_data = {}
        attendance_data = {}
        for key, value in request_data.items():
            if key in ["real_name"]:
                user_data[key] = value
            elif key in self.serializer_class().get_fields():
                attendance_data[key] = value
        return user_data, attendance_data

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = User.objects.get(id=instance.user_id)
        except (User.DoesNotExist, Attendance.DoesNotExist):
            return Result.FAIL_404_NOT_FOUND(msg="用户或信息不存在")

        user_data, attendance_data = self.split_data(request.data)

        # 判断并更新User表
        if user_data:
            for attr, val in user_data.items():
                setattr(user, attr, val)
            user.save()

        # 判断并更新Information表
        if attendance_data:
            for attr, val in attendance_data.items():
                setattr(instance, attr, val)
            instance.save()

        serializer = self.get_serializer(instance)
        return Result.OK_202_ACCEPTED(data=serializer.data)
