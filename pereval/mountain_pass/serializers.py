from rest_framework import serializers
from .models import User, Coords, PerevalAdded, PerevalImage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fam', 'name', 'otc', 'phone']

    def to_internal_value(self, data):
        # Проверяем, существует ли пользователь с данным email
        email = data.get('email')
        if not email:
            raise serializers.ValidationError({"email": "Это поле обязательно."})

        # Пытаемся найти пользователя с этим email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Если пользователь не найден, возвращаем данные для создания нового
            return super().to_internal_value(data)

        # Если пользователь найден, возвращаем его
        return {
            'email': user.email,
            'fam': user.fam,
            'name': user.name,
            'otc': user.otc,
            'phone': user.phone,
        }


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
        # fields = '__all__'
        fields = ['beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user', 'coords', 'images', 'level']

    # Отладка - проверка какое поле вызывает ошибку
    # def validate(self, data):
    #     # Отладка типа данных
    #     if not isinstance(data.get('user'), dict):
    #         raise serializers.ValidationError(f"user: Ожидался dictionary, получен {type(data.get('user'))}")
    #     if not isinstance(data.get('coords'), dict):
    #         raise serializers.ValidationError(f"coords: Ожидался dictionary, получен {type(data.get('coords'))}")
    #     if not isinstance(data.get('images'), list):
    #         raise serializers.ValidationError(f"images: Ожидался list, получен {type(data.get('images'))}")
    #     if not isinstance(data.get('level'), dict):
    #         raise serializers.ValidationError(f"level: Ожидался dictionary, получен {type(data.get('level'))}")
    #
    #     return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')

        # Добавляем пользователя, если его нет
        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'fam': user_data['fam'],
                'name': user_data['name'],
                'otc': user_data.get('otc'),
                'phone': user_data.get('phone'),
            }
        )

        # Добавляем координаты
        coords = Coords.objects.create(**coords_data)

        # Добавление уровней сложности
        validated_data.update({
            'winter': level_data.get('winter', ''),
            'summer': level_data.get('summer', ''),
            'autumn': level_data.get('autumn', ''),
            'spring': level_data.get('spring', ''),
        })

        # Добавление записи Перевала
        pereval_added = PerevalAdded.objects.create(user=user, coords=coords, **validated_data)

        # Обработка изображений
        for image_data in images_data:
            PerevalImage.objects.create(pereval=pereval_added, img_path=image_data['data'], title=image_data['title'])

        return pereval_added
