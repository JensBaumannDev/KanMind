from rest_framework import viewsets
from kanban_app.models import Board
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.db.models import Q
from .serializers import BoardSerializer
from .permissions import IsBoardMember


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get_queryset(self):
        return Board.objects.filter(
            Q(members__id=self.request.user.id) | Q(owner__id=self.request.user.id)
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            return Response(
                {"id": user.pk, "email": user.email, "fullname": user.get_full_name()}
            )
        else:
            return Response({"detail": "Email not found."}, status=404)
