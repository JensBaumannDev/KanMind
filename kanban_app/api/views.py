from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from kanban_app.models import Board, Comment, Task

from .permissions import (
    CanDeleteTask,
    IsBoardMember,
    IsBoardMemberForComment,
    IsBoardMemberForTask,
    IsBoardOwner,
    IsCommentAuthor,
)
from .serializers import (
    BoardDetailSerializer,
    BoardSerializer,
    BoardUpdateSerializer,
    CommentSerializer,
    TaskSerializer,
)


class BoardViewSet(viewsets.ModelViewSet):
    """CRUD for boards the requesting user owns or is a member of."""

    serializer_class = BoardSerializer
    queryset = Board.objects.all()

    def get_queryset(self):
        """Restrict the list view; detail actions rely on object-level permissions instead."""
        if self.action != "list":
            return Board.objects.all()
        return Board.objects.filter(
            Q(members__id=self.request.user.id) | Q(owner__id=self.request.user.id)
        ).distinct()

    def perform_create(self, serializer):
        """Set the requesting user as the board's owner."""
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        """Use a richer serializer for retrieve/update than for list/create."""
        if self.action == "retrieve":
            return BoardDetailSerializer
        if self.action == "update" or self.action == "partial_update":
            return BoardUpdateSerializer
        return BoardSerializer

    def get_permissions(self):
        """Only the owner may delete a board; any member may do everything else."""
        if self.action == "destroy":
            return [IsAuthenticated(), IsBoardOwner()]
        return [IsAuthenticated(), IsBoardMember()]


class EmailCheckView(APIView):
    """Look up a user by exact email address."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return the matching user, or 404 if no user has that email."""
        email = request.query_params.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            return Response(
                {"id": user.pk, "email": user.email, "fullname": user.get_full_name()}
            )
        else:
            return Response({"detail": "Email not found."}, status=404)


class TaskViewSet(viewsets.ModelViewSet):
    """Create/update/delete tasks; no list/retrieve action, those aren't in the spec."""

    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        """Record the requesting user as the task's creator."""
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        """Only the creator or the board owner may delete a task."""
        if self.action == "destroy":
            return [IsAuthenticated(), CanDeleteTask()]
        return [IsAuthenticated(), IsBoardMemberForTask()]


class AssignedToMeView(generics.ListAPIView):
    """List tasks where the requesting user is the assignee."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Restrict tasks to ones assigned to the requesting user."""
        return Task.objects.filter(assignee=self.request.user)


class ReviewingView(generics.ListAPIView):
    """List tasks where the requesting user is the reviewer."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Restrict tasks to ones the requesting user is reviewing."""
        return Task.objects.filter(reviewer=self.request.user)


class CommentListCreateView(generics.ListCreateAPIView):
    """List and create comments for a single task."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsBoardMemberForComment]

    def get_queryset(self):
        """Restrict comments to the task identified in the URL."""
        return Comment.objects.filter(task_id=self.kwargs["task_id"])

    def perform_create(self, serializer):
        """Set the comment's author and task from the request user and URL."""
        serializer.save(author=self.request.user, task_id=self.kwargs["task_id"])


class CommentDeleteView(generics.DestroyAPIView):
    """Delete a single comment; only the comment's author is allowed."""

    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated, IsCommentAuthor]
    lookup_url_kwarg = "comment_id"
