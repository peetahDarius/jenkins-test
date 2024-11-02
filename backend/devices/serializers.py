from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["id", "name", "max_clients", "max_capacity", "created_at", "updated_at", "created_by"]
        extra_kwargs = {"created_by": {"read_only": True}, "created_at": {"read_only": True}, "updated_at": {"read_only": True}}
