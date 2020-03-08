from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    email = serializers.CharField(source="user.email")
    image = serializers.URLField(required=False)
    address = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = Profile
        fields = (
            "id",
            "email",
            "image",
            "address",
            "phone_number",
            "created_at",
            "updated_at",
        )
