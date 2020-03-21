from rest_framework import serializers

from .models import ParcelDelivery


class ParcelDeliverySerializer(serializers.ModelSerializer):
    pickup_location = serializers.CharField(
        required=True, error_messages={"required": "Pickup location is required"}
    )
    destination = serializers.CharField(
        required=True, error_messages={"required": "Destination is required"}
    )
    present_location = serializers.CharField(required=False)
    weight = serializers.IntegerField(
        required=True, error_messages={"required": "Weight is required"}
    )
    quote = serializers.IntegerField(
        required=True, error_messages={"required": "Quote is required"}
    )

    class Meta:
        model = ParcelDelivery
        fields = (
            "id",
            "pickup_location",
            "destination",
            "present_location",
            "weight",
            "quote",
            "status",
            "order_number",
            "created_at",
            "updated_at",
            "is_deleted",
        )
        extra_kwargs = {
            "is_deleted": {"write_only": True},
        }
