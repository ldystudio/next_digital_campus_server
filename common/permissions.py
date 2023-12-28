from rest_framework.permissions import BasePermission, IsAuthenticated


class IsOwnerOperation(BasePermission):
    message = '只能操作自己的账户'

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class IsAdminUser(IsAuthenticated):
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view) and request.user.user_role == 'admin'
        )


class IsAdminOrTeacherUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.user_role in [
            'admin',
            'teacher',
        ]
