from rest_framework.permissions import BasePermission


class IsBoardMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user in obj.members.all() or request.user == obj.owner:
            return True

        return False
