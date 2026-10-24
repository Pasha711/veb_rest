from rest_framework import serializers
from .models import Origin, Coffee


class OriginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Origin
        fields = '__all__'


class CoffeeSerializer(serializers.ModelSerializer):
    origin_name = serializers.CharField(source='origin.country', read_only=True)

    class Meta:
        model = Coffee
        fields = '__all__'
