from django.shortcuts import render
from rest_framework import generics
from .models import TemperatureHumidity
from .serializer import TemperatureHumiditySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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
@csrf_exempt
def relay_control_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        relay_state = data.get('relay_state', None)

        if relay_state is not None:
            # Handle the relay state logic
            if relay_state == "true":
                # Code to turn the relay on (you can update database or logic accordingly)
                return JsonResponse({'message': 'Relay turned ON'}, status=200)
            elif relay_state == "false":
                # Code to turn the relay off
                return JsonResponse({'message': 'Relay turned OFF'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid relay state'}, status=400)
        else:
            return JsonResponse({'error': 'No relay state provided'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)