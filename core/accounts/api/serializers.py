from rest_framework.serializers import ModelSerializer
from ..models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "is_superuser"]
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user
