from rest_framework import permissions


class IsOwnerOrReadOnlyOrSuperuser(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view or edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        # Check if the object has an attribute named 'user'.
        owner = getattr(obj, 'user', None)
        if owner is not None:
            return owner == request.user or request.user.is_superuser
        # If there's no user attribute, deny permission.
        return False



class CanViewAndPostOnly(permissions.BasePermission):
    """
    Custom permission to only allow viewing and adding of objects.
    """

    def has_permission(self, request, view):
        # Only allow GET or POST requests
        if request.method in ['GET', 'POST']:
            return True
        return False