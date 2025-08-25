from rest_framework import serializers
from .models import CustomUser, Activity

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'password', 'email', 'age', 'height', 'weight']

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data["username"],
            email=validated_data.get("email", "")
        )
        user.set_password(validated_data["password"])  # ✅ hash password
        user.save()
        return user

    def update_password(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"

    def validate(self, data):
        if data.get("duration_minutes", 0) <= 0:
            raise serializers.ValidationError("Duration must be greater than 0.")
        if data.get("calories_burned", 0) < 0:
            raise serializers.ValidationError("Calories burned cannot be negative.")
        return data