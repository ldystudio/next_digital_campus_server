from rest_framework import serializers

from .models import Information


class ClassInformationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Information
        exclude = ("date_joined", "date_updated")
        read_only_fields = ("id", "date_joined", "date_updated")
