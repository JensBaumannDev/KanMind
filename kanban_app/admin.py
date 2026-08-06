from django.contrib import admin
from .models import Board, Task, Comment

# Register your models here.


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass