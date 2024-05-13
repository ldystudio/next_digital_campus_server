from django.db import transaction
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework_extensions.cache.decorators import cache_response
from snowflake.client import get_guid

from common.cache import CacheFnMixin
from common.permissions import IsOwnerMessage
from common.result import Result
from iam.models import User
from .models import Room, RoomType
from .serializers import RoomSerializer, RoomListSerializer


class RoomViewSet(
    CacheFnMixin, RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet
):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsOwnerMessage,)

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            request_user_id = self.request.user.id
            return queryset.filter(
                name__regex=rf"private-room-({request_user_id}&\d+)|(\d+&{request_user_id}$)"
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return RoomListSerializer
        return super().get_serializer_class()

    @cache_response(key_func="list_cache_key_func")
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Result.OK_200_SUCCESS(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Result.OK_200_SUCCESS(data=serializer.data)

    def create(self, request, *args, **kwargs):
        other_user_id = request.data.get("user_id", None)
        room_type = request.data.get("type", 1)

        instance = Room.objects.filter(
            name__in=[
                f"private-room-{request.user.id}&{other_user_id}",
                f"private-room-{other_user_id}&{request.user.id}",
            ],
            type=RoomType.PRIVATE.value,
        ).first()

        if not instance:
            try:
                User.objects.get(pk=other_user_id)
            except User.DoesNotExist:
                return Result.FAIL_400_INVALID_PARAM("无效的用户ID")

            with transaction.atomic():
                try:
                    instance = Room.objects.create(
                        pk=get_guid(),
                        name=f"private-room-{request.user.id}&{other_user_id}",
                        type=room_type,
                        host=request.user,
                    )
                    instance.members.set([request.user.id, other_user_id])
                except:
                    transaction.set_rollback(True)
                    return Result.FAIL_400_OPERATION("创建聊天室失败")

        serializer = RoomSerializer(instance=instance)
        return Result.OK_200_SUCCESS(data=serializer.data)
