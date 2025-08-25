from rest_framework import serializers
from .models import CustomUser, Activity

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "age", "height", "weight", "is_active", "is_staff", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            age=validated_data.get("age"),
            height=validated_data.get("height"),
            weight=validated_data.get("weight"),
        )
        return user


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]
