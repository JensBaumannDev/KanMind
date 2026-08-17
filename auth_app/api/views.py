from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegistrationSerializer


def build_auth_response(user, status_code):
    """Build the {token, fullname, email, user_id} response shared by registration and login."""
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {
            "token": token.key,
            "fullname": user.get_full_name(),
            "email": user.email,
            "user_id": user.pk,
        },
        status=status_code,
    )


class RegistrationView(generics.CreateAPIView):
    """Create a new user account and return an auth token."""

    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Validate the registration data, create the user, and return a token."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return build_auth_response(user, status.HTTP_201_CREATED)


class LoginView(APIView):
    """Authenticate a user by email/password and return an auth token."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Validate credentials and return a token for the authenticated user."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return build_auth_response(user, status.HTTP_200_OK)
