from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    """Validate registration data and create the resulting User."""

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
        """Ensure password and repeated_password match."""
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        """Create the User, using the email as username (login authenticates by email)."""
        fullname = validated_data["fullname"]
        first_name, last_name = fullname.split(" ", 1)
        email = validated_data["email"]
        return User.objects.create_user(
            username=email,
            email=email,
            password=validated_data["password"],
            first_name=first_name,
            last_name=last_name,
        )

    def validate_fullname(self, value):
        """Require at least a first and last name."""
        if " " not in value:
            raise serializers.ValidationError(
                "Fullname must contain at least a first and last name."
            )
        return value

    def validate_email(self, value):
        """Reject emails already tied to an existing user."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This user already exists.")
        return value


class LoginSerializer(serializers.Serializer):
    """Validate credentials and resolve them to the authenticated User."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, data):
        """Authenticate by email/password; authenticate() also rejects inactive users."""
        user = authenticate(
            request=self.context.get("request"),
            username=data.get("email"),
            password=data.get("password"),
        )
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        data["user"] = user
        return data
