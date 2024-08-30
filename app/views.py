from django.shortcuts import render
from rest_framework import generics
from .models import TemperatureHumidity
from .serializer import TemperatureHumiditySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

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

def temperature_humidity_history(request):
    history_data = TemperatureHumidity.objects.all().order_by('-timestamp')
    return render(request, 'history.html', {'history_data': history_data})

def history_view(request):
    date_query = request.GET.get('date')
    
    if date_query:
        selected_date = datetime.strptime(date_query, "%Y-%m-%d").date()
        readings = TemperatureHumidity.objects.filter(timestamp__date=selected_date).order_by('-timestamp')
    else:
        readings = TemperatureHumidity.objects.all().order_by('-timestamp')
    return render(request, 'history.html', {'readings': readings, 'date_query': date_query})

def save_reading(temperature, humidity):
    reading = TemperatureHumidity(temperature=temperature, humidity=humidity)
    reading.save()