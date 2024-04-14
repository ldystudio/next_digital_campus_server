from rest_framework.permissions import BasePermission, IsAuthenticated

from common.utils.decide import is_request_mapped_to_view, is_admin, is_teacher
from common.utils.gain import get_related_field_values_list
from teacher.models import Information as TeacherInformation


class IsOwnerAccount(BasePermission):
    message = "只能操作自己的账户"

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class IsOwnerOperation(IsAuthenticated):
    message = "只能对自己的实体操作"

    def has_object_permission(self, request, view, obj):
        # 管理员可以操作所有实体
        if is_admin(request):
            return True

        if is_teacher(request):
            if is_request_mapped_to_view(request, "CourseSettingsViewSet"):
                try:
                    teacher = request.user.teacher
                except TeacherInformation.DoesNotExist:
                    return False
                return teacher.id in get_related_field_values_list(obj.teacher)
            elif is_request_mapped_to_view(request, "ScoreEnterViewSet"):
                try:
                    teacher = request.user.teacher
                except TeacherInformation.DoesNotExist:
                    return False
                return obj.course_id in get_related_field_values_list(teacher.course)

        return obj.user.id == request.user.id


class IsAdminUser(IsAuthenticated):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view) and request.user.user_role == "admin"
        )


class IsAdminOrTeacherUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.user_role in [
            "admin",
            "teacher",
        ]


class IsAdminOrStudentUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.user_role in [
            "admin",
            "student",
        ]
