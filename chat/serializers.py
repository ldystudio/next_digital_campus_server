from django.db.models import Q
from pydash import omit
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from iam.serializers import UserSimpleSerializer
from .models import Room, Message


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = UserSimpleSerializer()
    room = PrimaryKeyRelatedField(read_only=True, pk_field=serializers.CharField())

    def to_representation(self, instance: Room):
        ret = super().to_representation(instance)
        ret["userId"] = ret["user"]["id"]
        ret["avatar"] = ret["user"]["avatar"]
        ret["name"] = ret["user"]["real_name"]
        ret["time"] = ret.pop("created_at")
        ret["message"] = ret.pop("text")
        return omit(ret, ["user", "room", "is_read", "file"])

    class Meta:
        model = Message
        fields = "__all__"
        depth = 1


class RoomSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    last_message = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)
    members = UserSimpleSerializer(many=True, read_only=True)
    host = UserSimpleSerializer()

    def get_last_message(self, obj: Room):
        return MessageSerializer(obj.messages.order_by("created_at").last()).data

    class Meta:
        model = Room
        fields = ["id", "name", "host", "messages", "members", "last_message"]
        read_only_fields = ["id", "messages", "last_message"]


class RoomListSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    def to_representation(self, instance: Room):
        ret = super().to_representation(instance)
        other_members = instance.members.filter(
            ~Q(id=self.context.get("request").user.id)
        ).first()
        last_message = instance.messages.order_by("-created_at").first()
        count = instance.messages.filter(is_read=False).count()
        ret.update(
            {
                "name": other_members.real_name,
                "avatar": other_members.avatar,
                "message": getattr(last_message, "text", ""),
                "count": count,
                "time": getattr(last_message, "created_at", None),
            }
        )
        return ret

    class Meta:
        model = Room
        fields = ["id"]


class RoomRetrieveSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    def to_representation(self, instance: Room):
        ret = super().to_representation(instance)
        request_user_id = self.context.get("request_user").id
        other_members = instance.members.filter(~Q(id=request_user_id)).first()
        ret["other_members"] = {
            "real_name": other_members.real_name,
            "user_role": other_members.user_role,
        }
        return ret

    class Meta:
        model = Room
        fields = ["messages"]
