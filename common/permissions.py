from rest_framework.permissions import BasePermission, IsAuthenticated

from common.utils.decide import is_request_mapped_to_view, is_admin, is_teacher
from common.utils.gain import get_related_field_values_list
from course.models import Setting as Course


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
            teacher = request.user.teacher

            if is_request_mapped_to_view(request, "CourseSettingsViewSet"):
                return teacher.id in get_related_field_values_list(obj.teacher)
            elif is_request_mapped_to_view(request, "ScoreInformationViewSet"):
                return obj.course_id in get_related_field_values_list(
                    teacher.course
                ).union(
                    get_related_field_values_list(
                        Course.objects.filter(classes__in=teacher.classes.all())
                    )
                )

        return obj.user.id == request.user.id


class IsOwnerMessage(IsAuthenticated):
    message = "只能对自己的消息操作"

    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()


class IsAdminUser(IsAuthenticated):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view) and request.user.user_role == "admin"
        )


class IsTeacherOrAdminUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.user_role in [
            "admin",
            "teacher",
        ]


class IsStudentOrAdminUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.user_role in [
            "admin",
            "student",
        ]


class IsStudent(IsAuthenticated):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and request.user.user_role == "student"
        )
