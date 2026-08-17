from rest_framework.exceptions import NotFound
from rest_framework.permissions import BasePermission

from kanban_app.models import Board, Task


class IsBoardMember(BasePermission):
    """Allow board members and the board owner."""

    def has_object_permission(self, request, view, obj):
        if request.user in obj.members.all() or request.user == obj.owner:
            return True
        return False


class IsBoardOwner(BasePermission):
    """Allow only the board owner."""

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsBoardMemberForTask(BasePermission):
    """Require board membership: from request data on create, from the task's board otherwise."""

    def has_permission(self, request, view):
        """On create, require membership of the board named in the request body."""
        if view.action != "create":
            return True

        board = Board.objects.filter(id=request.data.get("board")).first()
        if board is None:
            raise NotFound("Board not found.")

        return request.user in board.members.all() or request.user == board.owner

    def has_object_permission(self, request, view, obj):
        """On update, require membership of the task's existing board."""
        if request.user in obj.board.members.all() or request.user == obj.board.owner:
            return True
        return False


class CanDeleteTask(BasePermission):
    """Allow only the task's creator or the board owner to delete it."""

    def has_object_permission(self, request, view, obj):
        if request.user == obj.created_by or request.user == obj.board.owner:
            return True
        return False


class IsBoardMemberForComment(BasePermission):
    """Require membership on the board the task (from the URL) belongs to."""

    def has_permission(self, request, view):
        task = Task.objects.filter(id=view.kwargs.get("task_id")).first()
        if task is None:
            raise NotFound("Task not found.")
        return (
            request.user in task.board.members.all() or request.user == task.board.owner
        )


class IsCommentAuthor(BasePermission):
    """Allow only the comment's own author."""

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        return False
