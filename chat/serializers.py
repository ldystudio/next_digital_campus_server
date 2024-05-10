from rest_framework import serializers

from iam.serializers import UserSimpleSerializer
from .models import Room, Message


class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = UserSimpleSerializer()

    def get_created_at_formatted(self, obj: Message):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")

    class Meta:
        model = Message
        exclude = []
        depth = 1


class RoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)

    def get_last_message(self, obj: Room):
        return MessageSerializer(obj.messages.order_by("created_at").last()).data

    class Meta:
        model = Room
        fields = ["pk", "name", "host", "messages", "current_users", "last_message"]
        depth = 1
        read_only_fields = ["messages", "last_message"]
