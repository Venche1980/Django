from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # Проверяем, что у пользователя не больше 10 открытых объявлений
        request = self.context["request"]

        # Если создаем новое объявление или меняем статус с CLOSED на OPEN
        if request.method == "POST" or data.get("status") != "CLOSED":
            # Подсчитываем количество открытых объявлений пользователя
            open_advertisements_count = Advertisement.objects.filter(
                creator=request.user,
                status=AdvertisementStatusChoices.OPEN
            ).count()

            # Если уже 10 открытых объявлений, выбрасываем ошибку
            if open_advertisements_count >= 10:
                raise ValidationError("У пользователя не может быть больше 10 открытых объявлений")

        return data