from django.shortcuts import render
from rest_framework import generics
from .models import TemperatureHumidity
from .serializer import TemperatureHumiditySerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class TemperatureHumidityDetailView(generics.RetrieveAPIView):
    queryset = TemperatureHumidity.objects.all()
    serializer_class = TemperatureHumiditySerializer

class TemperatureHumidityListView(generics.ListAPIView):
    queryset = TemperatureHumidity.objects.all()
    serializer_class = TemperatureHumiditySerializer


class TemperatureHumidityCreateAPIView(generics.CreateAPIView):
    queryset = TemperatureHumidity.objects.all()
    serializer_class = TemperatureHumiditySerializer

class LatestTemperatureHumidityAPIView(APIView):
    def get(self, request, *args, **kwargs):
        latest_record = TemperatureHumidity.objects.latest('timestamp')
        return Response({
            'temperature': latest_record.temperature,
            'humidity': latest_record.humidity
        })
    
def temperature_monitor(request):
    return render(request, 'temperature.html')

