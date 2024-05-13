from enum import Enum

from django.db import models
from iam.models import User


class RoomType(Enum):
    PRIVATE = 1
    GROUP = 2


class Room(models.Model):
    name = models.CharField(
        db_comment="聊天室名称", max_length=255, null=True, blank=True, unique=True
    )
    room_type_choices = ((1, "私聊"), (2, "群聊"))
    type = models.SmallIntegerField(
        db_comment="聊天室类型", choices=room_type_choices, default=1
    )
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="host_rooms")
    members = models.ManyToManyField(User, related_name="rooms", blank=True)

    def __str__(self):
        return f"Room({self.name} {self.host})"


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField(db_comment="聊天内容", max_length=500)
    is_read = models.BooleanField(db_comment="是否已读", default=False)
    file = models.FileField(
        db_comment="聊天文件", upload_to="chat_files", null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    created_at = models.DateTimeField(db_comment="创建时间", auto_now_add=True)

    def __str__(self):
        return f"Message({self.user} {self.room})"
