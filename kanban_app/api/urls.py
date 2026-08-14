from django.urls import path
from rest_framework import routers
from .views import BoardViewSet, TaskViewSet, EmailCheckView, AssignedToMeView, ReviewingView

router = routers.SimpleRouter()
router.register(r"boards", BoardViewSet, basename="board")
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("email-check/", EmailCheckView.as_view()),
    path("tasks/assigned-to-me/", AssignedToMeView.as_view()),
    path("tasks/reviewing/", ReviewingView.as_view())
] + router.urls

