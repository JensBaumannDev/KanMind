from django.urls import path
from rest_framework import routers

from .views import (
    AssignedToMeView,
    BoardViewSet,
    CommentDeleteView,
    CommentListCreateView,
    EmailCheckView,
    ReviewingView,
    TaskViewSet,
)

router = routers.SimpleRouter()
router.register(r"boards", BoardViewSet, basename="board")
router.register(r"tasks", TaskViewSet, basename="task")

board_detail_no_slash = BoardViewSet.as_view(
    {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path("email-check/", EmailCheckView.as_view()),
    path("tasks/assigned-to-me/", AssignedToMeView.as_view()),
    path("tasks/reviewing/", ReviewingView.as_view()),
    path("tasks/<int:task_id>/comments/", CommentListCreateView.as_view()),
    path("tasks/<int:task_id>/comments/<int:comment_id>/", CommentDeleteView.as_view()),
    path("boards/<int:pk>", board_detail_no_slash),
] + router.urls
