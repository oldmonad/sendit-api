from rest_framework.exceptions import ValidationError

from .models import ParcelDelivery


def parcel_not_found():
    raise ValidationError(detail={"error": "Parcel delivery not found"})


def get_parcel(id):
    try:
        return ParcelDelivery.objects.get(id=id)
    except Exception:
        parcel_not_found()
