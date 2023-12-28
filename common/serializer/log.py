from rest_framework import serializers
from rest_framework_tracking.models import APIRequestLog


class APIRequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIRequestLog
        exclude = ("response", "errors")


class APIRequestResponseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIRequestLog
        fields = ("response",)


class APIRequestErrorsLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIRequestLog
        fields = ("errors",)
