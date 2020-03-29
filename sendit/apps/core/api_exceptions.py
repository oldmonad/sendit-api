from rest_framework.exceptions import APIException


class ResourceDoesNotExist(APIException):
    status_code = 400
    default_detail = "The requested resource does not exist."


class UnathorizedException(APIException):
    status_code = 403
    default_detail = "You do not have permission to perform this action."
