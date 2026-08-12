from rest_framework.permissions import BasePermission

from kanban_app.models import Board


class IsBoardMember(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user in obj.members.all() or request.user == obj.owner:
            return True
        return False


class IsBoardOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsBoardMemberForTask(BasePermission):

    def has_permission(self, request, view):
        if view.action != "create":
            return True

        board = Board.objects.filter(id=request.data.get("board")).first()
        if board is None:
            return False

        return request.user in board.members.all() or request.user == board.owner

    def has_object_permission(self, request, view, obj):
        if request.user in obj.board.members.all() or request.user == obj.board.owner:
            return True
        return False


class CanDeleteTask(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.created_by or request.user == obj.board.owner:
            return True
        return False
