from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """This class creates permissions for owners of a resource and admin"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff


class IsAdminOnly(permissions.BasePermission):
    """This class creates permissions for get method for admins only"""

    def has_permission(self, request, view):
        if request.method == "GET":
            return request.user.is_staff
        return True
