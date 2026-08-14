from rest_framework import viewsets, generics
from kanban_app.models import Board, Task, Comment
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
    CommentSerializer,
)
from .permissions import (
    IsBoardMember,
    IsBoardOwner,
    IsBoardMemberForTask,
    CanDeleteTask,
    IsBoardMemberForComment,
    IsCommentAuthor,
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


class AssignedToMeView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)


class ReviewingView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsBoardMemberForComment]

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs["task_id"])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, task_id=self.kwargs["task_id"])


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsCommentAuthor]
    lookup_url_kwarg = "comment_id"
