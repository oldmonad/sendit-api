from .api_exceptions import UnathorizedException


def user_or_admin(user, parcel):
    if user == parcel.user or user.is_staff:
        return True
    raise UnathorizedException
