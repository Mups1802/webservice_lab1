from rest_framework import serializers
from .models import TemperatureHumidity

class TemperatureHumiditySerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureHumidity
        fields = ['temperature', 'humidity', 'timestamp']
