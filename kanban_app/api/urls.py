from django.urls import path
from rest_framework import routers
from .views import BoardViewSet, EmailCheckView

router = routers.SimpleRouter()
router.register(r'boards', BoardViewSet)
urlpatterns = [
    path('email-check/', EmailCheckView.as_view()),
] + router.urls