"""
Custom Permissions for the REST API.
"""
from rest_framework import permissions

from programs.apps.core.constants import Role


class IsAdminGroupOrReadOnly(permissions.IsAuthenticated):
    """
    Allow read-only access for any authenticated user, but require membership
    in the ADMINS group for writes.
    """

    def has_permission(self, request, view):
        return (
            super(IsAdminGroupOrReadOnly, self).has_permission(request, view) and
            request.method in permissions.SAFE_METHODS or
            request.user.groups.filter(name=Role.ADMINS).exists()
        )


class IsAdminGroup(permissions.IsAuthenticated):
    """
    Require membership in the ADMINS group for read or write access.
    """

    def has_permission(self, request, view):
        return (
            super(IsAdminGroup, self).has_permission(request, view) and
            request.user.groups.filter(name=Role.ADMINS).exists()
        )
