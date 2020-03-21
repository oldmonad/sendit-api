from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from sendit.apps.core.base_model import CommonFieldsMixin


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, full_name, email, password=None):
        """Create and return a `User` with an email, full name and password."""
        if full_name is None:
            raise TypeError("Users must have a name.")

        if email is None:
            raise TypeError("Users must have an email address.")

        user = self.model(full_name=full_name, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, full_name, email, password):
        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(full_name, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, CommonFieldsMixin):
    full_name = models.CharField(db_index=True, max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first and last name. Since we do
        not store the user's real name, we return their full name instead.
        """
        return self.full_name

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their full name instead.
        """
        return self.full_name

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token`
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JWT that stores this user's email and has an expiry
        date set to 1 day into the future.
        """

        dt = datetime.now() + timedelta(days=1)
        data = {
            "email": self.email,
            "active": self.is_active,
            "exp": int(dt.strftime("%s")),
        }
        token = jwt.encode(data, settings.SECRET_KEY, algorithm="HS256")

        return token.decode("utf-8")
