from rest_framework import permissions


class IsOrganisatorOrAdmin(permissions.BasePermission):
    """Autorise l'accès aux organisateurs et administrateurs."""

    def has_permission(self, request, view):
        # La vérification de l'authentification et du token JWT est gérée par DRF.
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.user_type == 'organisator' or request.user.is_superuser)
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Superusers have full access
        if request.user.is_superuser:
            return True

        # Allow access if the user is the owner
        if hasattr(obj, 'user'):
            return obj.user == request.user


class MessagePermission(permissions.BasePermission):
    """Autorise l'accès aux superusers, expéditeurs ou destinataires du message."""

    def has_object_permission(self, request, view, obj):
        # Permet l'accès au superuser, à l'expéditeur et au destinataire du message.
        return (
            request.user.is_superuser or
            obj.sender == request.user or
            obj.recipient == request.user
        )
