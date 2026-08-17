from django.contrib.auth.models import User
from rest_framework import serializers

from kanban_app.models import Board, Comment, Task


class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "members",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
        ]
        extra_kwargs = {"members": {"write_only": True}}

    member_count = serializers.SerializerMethodField()

    def get_member_count(self, obj):
        return obj.members.count()

    ticket_count = serializers.SerializerMethodField()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    tasks_to_do_count = serializers.SerializerMethodField()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status="to-do").count()

    tasks_high_prio_count = serializers.SerializerMethodField()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority="high").count()

    owner_id = serializers.IntegerField(read_only=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "fullname",
        ]

    fullname = serializers.SerializerMethodField()

    def get_fullname(self, obj):
        return obj.get_full_name()


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "assignee_id",
            "reviewer",
            "reviewer_id",
            "due_date",
            "comments_count",
        ]

    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def validate(self, attrs):
        board = attrs.get("board") or (self.instance.board if self.instance else None)
        assignee = attrs.get("assignee")
        reviewer = attrs.get("reviewer")

        if assignee and assignee not in board.members.all() and assignee != board.owner:
            raise serializers.ValidationError("Assignee must be a board member.")
        if reviewer and reviewer not in board.members.all() and reviewer != board.owner:
            raise serializers.ValidationError("Reviewer must be a board member.")
        if self.instance and "board" in attrs and attrs["board"] != self.instance.board:
            raise serializers.ValidationError("Board cannot be changed.")
        return attrs

    assignee_id = serializers.PrimaryKeyRelatedField(
        source="assignee",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    reviewer_id = serializers.PrimaryKeyRelatedField(
        source="reviewer",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )


class BoardDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "owner_id",
            "members",
            "tasks",
        ]

    members = UserSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    owner_id = serializers.IntegerField(read_only=True)


class BoardUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "members",
            "members_data",
            "owner_data",
        ]
        extra_kwargs = {"members": {"write_only": True}}

    owner_data = UserSerializer(source="owner", read_only=True)
    members_data = UserSerializer(source="members", many=True, read_only=True)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]

    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return obj.author.get_full_name()
