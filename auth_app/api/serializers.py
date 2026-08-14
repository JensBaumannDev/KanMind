from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(
        max_length=100,
    )
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "fullname",
            "email",
            "password",
            "repeated_password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        fullname = validated_data.get("fullname")
        email = validated_data.get("email")
        password = validated_data.get("password")

        first_name, last_name = fullname.split(" ", 1)

        return User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

    def validate_fullname(self, value):
        if " " not in value:
            raise serializers.ValidationError(
                "Fullname must contain at least a first and last name."
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This user already exists.")
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("The user is currently deactivated.")

        data["user"] = user
        return data
