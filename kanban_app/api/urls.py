from django.urls import path
from rest_framework import routers
from .views import BoardViewSet, TaskViewSet, EmailCheckView

router = routers.SimpleRouter()
router.register(r"boards", BoardViewSet, basename="board")
router.register(r"tasks", TaskViewSet, basename="task")
urlpatterns = [
    path("email-check/", EmailCheckView.as_view()),
] + router.urls
