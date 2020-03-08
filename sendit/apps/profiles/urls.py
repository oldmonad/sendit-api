from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
    path(
        "users/<str:email>/",
        views.ProfileRetrieveAPIView.as_view(),
        name="user_profile",
    ),
    path("profiles/", views.ListProfile.as_view(), name="profile_list"),
]
