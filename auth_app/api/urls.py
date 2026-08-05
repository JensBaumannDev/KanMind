from django.urls import path
from auth_app.api.views import RegistrationView, LoginView

urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('login/', LoginView.as_view())
]