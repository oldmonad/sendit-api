import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from dotenv import load_dotenv

from sendit.apps.core.helpers.mail_handler import mail_handler
from sendit.apps.profiles.models import Profile

from .models import User

load_dotenv()


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):
    if instance and created:
        message_body = "Welcome to the Sendit platform. \
            Please verify that you requested to use this email address on this platform, \
            if you did not make this action, please ignore this \
            message. Click on the link below to verify your account, \
            Be advised that this link would expire in 24 hours."
        uid = urlsafe_base64_encode(force_bytes(instance.id))
        email_data = [
            "Sendit: Verification email",
            message_body,
            f"{os.getenv('VERIFICATION_LINK').strip()}/{uid}",
            instance.full_name.split(" ", 1)[0].capitalize(),
            "VERIFY EMAIL",
            "",
            "",
        ]
        mail_handler.delay(
            "email_template.html",
            email_data,
            "Sendit Account Verification",
            [instance.email,],  # noqa
        )

        instance.profile = Profile.objects.create(user=instance)
        return True
