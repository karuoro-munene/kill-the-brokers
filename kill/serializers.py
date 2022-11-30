from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from kill.models import Profile, Product


def validate_password(password):
    password_validation.validate_password(password)
    return password


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())],
    )
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        account = get_user_model().objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return account

    class Meta(object):
        model = get_user_model()
        fields = ("id", "email","password")


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "last_login",
            "is_superuser",
            "email",
            "is_active",
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
