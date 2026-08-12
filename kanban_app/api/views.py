from rest_framework import viewsets
from kanban_app.models import Board, Task
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.db.models import Q
from .serializers import (
    BoardSerializer,
    BoardDetailSerializer,
    BoardUpdateSerializer,
    TaskSerializer,
)
from .permissions import (
    IsBoardMember,
    IsBoardOwner,
    IsBoardMemberForTask,
    CanDeleteTask,
)


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(
            Q(members__id=self.request.user.id) | Q(owner__id=self.request.user.id)
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BoardDetailSerializer
        if self.action == "update" or self.action == "partial_update":
            return BoardUpdateSerializer
        return BoardSerializer

    def get_permissions(self):
        if self.action == "destroy":
            return [IsAuthenticated(), IsBoardOwner()]
        return [IsAuthenticated(), IsBoardMember()]


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


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        if self.action == "destroy":
            return [IsAuthenticated(), CanDeleteTask()]
        return [IsAuthenticated(), IsBoardMemberForTask()]
