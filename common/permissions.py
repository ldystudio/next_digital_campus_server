from rest_framework import permissions


class IsOwnerOperation(permissions.BasePermission):
    message = '只能操作自己的账户'

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
