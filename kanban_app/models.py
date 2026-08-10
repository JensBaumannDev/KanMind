from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=250)
    members = models.ManyToManyField(User)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_boards"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Board"
        ordering = ["title"]


class Task(models.Model):
    STATUS_CHOICES = [
        ("to-do", "To Do"),
        ("in-progress", "In Progress"),
        ("review", "In Review"),
        ("done", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_tasks"
    )
    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviewer_tasks",
    )
    due_date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Task"
        ordering = ["due_date"]


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="authored_comments"
    )
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    content = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.author},{self.content}"

    class Meta:
        verbose_name = "Comment"
        ordering = ["created_at"]
