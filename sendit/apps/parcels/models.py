from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.crypto import get_random_string

from sendit.apps.authentication.models import User
from sendit.apps.core.base_model import CommonFieldsMixin, SpecialFieldsMixin
from sendit.apps.core.helpers.enum import Status


class ParcelDelivery(CommonFieldsMixin, SpecialFieldsMixin):
    user = models.ForeignKey(
        User, related_name="parcel_deliveries", on_delete=models.CASCADE
    )
    pickup_location = models.CharField(db_index=True, max_length=255)
    destination = models.CharField(db_index=True, max_length=255)
    present_location = models.CharField(db_index=True, max_length=255, null=True)
    weight = models.IntegerField(db_index=True)
    quote = models.IntegerField(db_index=True)
    status = models.CharField(
        db_index=True,
        max_length=255,
        choices=Status.choices(),
        default=Status.PENDING.value,
    )
    order_number = models.CharField(
        db_index=True, max_length=225, unique=True, blank=True
    )

    def __str__(self):
        return f"{self.pickup_location}{self.destination}{self.weight}{self.quote}"

    def random_string(self):
        """Generates a random string"""
        return get_random_string(length=10, allowed_chars="1234567890")

    def create_order_number(self):
        """Method to create order number"""

        order_number = self.random_string()
        new_order_number = order_number

        while ParcelDelivery.objects.filter(order_number=order_number).exists():
            new_order_number = self.random_string()

        return new_order_number

    def save(self, *args, **kwargs):
        """
        Ensure that before a parcel is saved,
        it must have a order number created
        """

        if not self.order_number:
            self.order_number = self.create_order_number()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
