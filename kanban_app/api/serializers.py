from rest_framework import serializers
from kanban_app.models import Board


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
