from rest_framework import serializers
from .models import User, Coords, PerevalImage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone']


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class PerevalImageSerializer(serializers.ModelSerializer):
    data = serializers.CharField(write_only=True)

    class Meta:
        model = PerevalImage
        fields = ['data', 'title']


class PerevalAddedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    images = PerevalImageSerializer(many=True)
    level = serializers.DictField(write_only=True)

    class Meta:
        model = PerevalAdded
        fields = ['beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user', 'coords', 'images', 'level']

    # Отладка - проверка какое поле вызывает ошибку
    def validate(self, data):
        # Отладка типа данных
        if not isinstance(data.get('user'), dict):
            raise serializers.ValidationError(f"user: Ожидался dictionary, получен {type(data.get('user'))}")
        if not isinstance(data.get('coords'), dict):
            raise serializers.ValidationError(f"coords: Ожидался dictionary, получен {type(data.get('coords'))}")
        if not isinstance(data.get('images'), list):
            raise serializers.ValidationError(f"images: Ожидался list, получен {type(data.get('images'))}")
        if not isinstance(data.get('level'), dict):
            raise serializers.ValidationError(f"level: Ожидался dictionary, получен {type(data.get('level'))}")

        return data

    def create(self, validated_data):
        # Получение и удаление вложенных данных
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')

        # Добавляем пользователя
        user = User.objects.create(email=user_data['email'], defaults=user_data)

        # Добавляем координаты
        coords = Coords.objects.create(**coords_data)

        # Добавление записи Перевала
        pereval_added = PerevalAdded.objects.create(user=user, coords=coords, **validated_data)

        # Обрабатываем уровни сложности
        pereval_added.winter = level_data.get('winter', '')
        pereval_added.summer = level_data.get('summer', '')
        pereval_added.autumn = level_data.get('autumn', '')
        pereval_added.spring = level_data.get('spring', '')
        pereval_added.save()

        # Добавляем изображения
        for image in images_data:
            PerevalImage.objects.create(pereval=pereval_added, img_path=image['data'])

        return pereval_added
