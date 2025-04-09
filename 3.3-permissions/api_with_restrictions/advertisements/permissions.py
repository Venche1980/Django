from rest_framework.permissions import BasePermission, IsAuthenticated


class IsOwner(BasePermission):
    """Проверка, что пользователь является владельцем объявления."""

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
