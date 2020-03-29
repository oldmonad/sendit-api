from django.urls import path

from . import views

app_name = "parcels"

urlpatterns = [
    path("parcels/", views.ListCreateParcelDelivery.as_view(), name="parcels"),
    path(
        "parcels/<str:id>/",
        views.RetrieveUpdateParcelDelivery.as_view(),
        name="parcel_details",
    ),
    path(
        "users/<str:user_id>/parcels", views.UserParcels.as_view(), name="user_parcels"
    ),
]
