from django.db import models

from sendit.apps.core.base_model import CommonFieldsMixin


class Profile(CommonFieldsMixin):
    user = models.OneToOneField("authentication.User", on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    phone_number = models.TextField(blank=True)
    image = models.URLField(
        blank=True,
        default="https://d1nhio0ox7pgb.cloudfront.net/_img/o_collection_png/green_dark_grey/512x512/plain/user.png",
    )

    def __str__(self):
        return self.user.full_name

    class Meta:
        ordering = ["created_at"]
