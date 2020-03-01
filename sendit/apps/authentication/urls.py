from django.urls import path

from .views import (
    HomeView,
    LoginAPIView,
    RegistrationAPIView,
    UserRetrieveUpdateAPIView,
)

app_name = "authentication"

urlpatterns = [
    path("", HomeView.as_view()),
    path("users/login/", LoginAPIView.as_view(), name="login"),
    path("user/", UserRetrieveUpdateAPIView.as_view(), name="current_user"),
    path("users/", RegistrationAPIView.as_view(), name="signup"),
]
