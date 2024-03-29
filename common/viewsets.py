from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework_tracking.mixins import LoggingMixin

from common.permissions import IsAdminUser, IsOwnerOperation
from common.result import Result
from iam.models import User


class ReadOnlyModelViewSetFormatResult(LoggingMixin, ReadOnlyModelViewSet):
    logging_methods = ["GET"]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)


class RetrieveModelViewSetFormatResult(
    LoggingMixin, mixins.RetrieveModelMixin, GenericViewSet
):
    logging_methods = ["GET"]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)


class ModelViewSetFormatResult(LoggingMixin, ModelViewSet):
    permission_classes = (IsOwnerOperation,)
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend)
    logging_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    def list(self, request, *args, **kwargs):
        # 非管理员只能查询自己的list
        user = request.user
        if user.user_role == "admin":
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.filter_queryset(self.get_queryset().filter(user_id=user.id))
        # 分页处理
        serializer = self.get_serializer(self.paginate_queryset(queryset), many=True)
        paginated_response = self.get_paginated_response(serializer.data)
        return Result.OK_200_SUCCESS(data=paginated_response.data)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Result.OK_201_CREATED(data=response.data)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Result.OK_202_ACCEPTED(data=response.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Result.OK_202_ACCEPTED(msg="删除成功")


class ReadWriteModelViewSetFormatResult(
    LoggingMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    permission_classes = (IsOwnerOperation,)
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend)
    logging_methods = ["GET", "PATCH"]
    user_fields = []

    def split_data(self, request_data):
        user_data = {}
        model_data = {}
        for key, value in request_data.items():
            if key in self.user_fields:
                user_data[key] = value
            elif key in self.serializer_class().get_fields():
                model_data[key] = value
        return user_data, model_data

    def get_permissions(self):
        # 仅对“list”操作应用IsAdminUser权限
        return (IsAdminUser(),) if self.action == "list" else super().get_permissions()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = User.objects.get(id=instance.user_id)
        except (User.DoesNotExist, self.get_queryset().model.DoesNotExist):
            return Result.FAIL_404_NOT_FOUND(msg="用户或信息不存在")

        user_data, model_data = self.split_data(request.data)

        if user_data:
            for attr, val in user_data.items():
                setattr(user, attr, val)
            user.save()

        if model_data:
            for attr, val in model_data.items():
                setattr(instance, attr, val)
            instance.save()

        serializer = self.get_serializer(instance)
        return Result.OK_202_ACCEPTED(data=serializer.data)
