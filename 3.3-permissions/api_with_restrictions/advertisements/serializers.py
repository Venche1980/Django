from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Advertisement


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
                  'status', 'created_at', )

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
        user = self.context["request"].user

        # Определяем, какое действие выполняется (создание или обновление)
        creating_ad = not self.instance

        # Для обновления проверяем, не меняется ли статус с CLOSED на OPEN
        changing_to_open = False
        if not creating_ad and self.instance.status == AdvertisementStatusChoices.CLOSED and \
                data.get('status') == AdvertisementStatusChoices.OPEN:
            changing_to_open = True

        # Если создаем новое объявление или меняем статус с CLOSED на OPEN
        if (creating_ad and data.get('status', AdvertisementStatusChoices.OPEN) == AdvertisementStatusChoices.OPEN) or \
                changing_to_open:
            # Подсчитываем количество открытых объявлений пользователя
            open_advertisements_count = Advertisement.objects.filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN
            ).count()

            # Если уже 10 открытых объявлений, выбрасываем ошибку
            if open_advertisements_count >= 10:
                raise ValidationError("У пользователя не может быть больше 10 открытых объявлений")

        return data