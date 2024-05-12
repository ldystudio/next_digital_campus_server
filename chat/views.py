from django.db import transaction
from rest_framework.generics import CreateAPIView
from snowflake.client import get_guid

from common.result import Result
from iam.models import User
from .models import Room, RoomType
from .serializers import RoomSerializer


class RoomAPIView(CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def post(self, request, *args, **kwargs):
        other_user_id = request.data.get("user_id", None)
        room_type = request.data.get("type", 1)

        instance = Room.objects.filter(
            name__in=[
                f"private-room-{request.user.id}&{other_user_id}",
                f"private-room-{other_user_id}&{request.user.id}",
            ],
            type=room_type,
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

        serializer = RoomSerializer(instance)
        return Result.OK_200_SUCCESS(data=serializer.data)
