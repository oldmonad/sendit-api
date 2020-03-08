""" Common fields mixin """

import uuid

from django.db import models


class CommonFieldsMixin(models.Model):
    """Add created_at and updated_at fields."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        """Define metadata options."""

        abstract = True
