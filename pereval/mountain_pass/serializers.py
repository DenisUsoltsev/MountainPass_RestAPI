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