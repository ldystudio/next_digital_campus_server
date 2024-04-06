from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_tracking.mixins import LoggingMixin

from common.permissions import IsAdminUser, IsOwnerOperation
from common.result import Result
from common.utils.cache import CacheFnMixin
from iam.models import User


class ReadOnlyModelViewSetFormatResult(
    LoggingMixin, CacheFnMixin, ReadOnlyModelViewSet
):
    logging_methods = ["GET"]

    @cache_response(key_func="list_cache_key_func")
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)

    @cache_response(key_func="object_cache_key_func")
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


class ModelViewSetFormatResult(LoggingMixin, CacheFnMixin, ModelViewSet):
    permission_classes = (IsOwnerOperation,)
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend)
    logging_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    @cache_response(key_func="list_cache_key_func")
    def list(self, request, *args, **kwargs):
        user = request.user
        # 非管理员只能查询自己的list
        if user.user_role == "admin":
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.filter_queryset(self.get_queryset().filter(user_id=user.id))
        # 分页处理
        serializer = self.get_serializer(self.paginate_queryset(queryset), many=True)
        paginated_response = self.get_paginated_response(serializer.data)
        return Result.OK_200_SUCCESS(data=paginated_response.data)

    @cache_response(key_func="object_cache_key_func")
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Result.OK_201_CREATED(data=response.data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Result.OK_202_ACCEPTED(data=response.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Result.OK_202_ACCEPTED(msg="删除成功")


class ReadWriteModelViewSetFormatResult(
    LoggingMixin,
    CacheFnMixin,
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

    @cache_response(key_func="list_cache_key_func")
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)

    @cache_response(key_func="object_cache_key_func")
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        try:
            instance = self.get_object()
            user = User.objects.get(id=instance.user_id)
        except (User.DoesNotExist, self.get_queryset().model.DoesNotExist):
            return Result.FAIL_404_NOT_FOUND(msg="用户或信息不存在")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        user_data, model_data = self.split_data(request.data)

        if user_data:
            for attr, val in user_data.items():
                setattr(user, attr, val)
            user.save()

        if model_data:
            for attr, val in model_data.items():
                if attr == "classes":  # 如果属性为 classes，则使用 set 方法
                    instance.classes.set(val)
                else:
                    setattr(instance, attr, val)
            instance.save()

        self.perform_update(serializer)
        return Result.OK_202_ACCEPTED(data=serializer.data)
