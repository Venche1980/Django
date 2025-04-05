from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet

from .filters import AdvertisementFilter
from .models import Advertisement
from .serializers import AdvertisementSerializer
class IsOwner(IsAuthenticated):
    """Проверка, что пользователь является владельцем объявления."""

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated()]
        elif self.action == "destroy":
            return [IsOwner()]
        return []

    def destroy(self, request, *args, **kwargs):
        """Удаление объявления."""
        return super().destroy(request, *args, **kwargs)