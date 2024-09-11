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

relay_state = False  # Initially, relay is OFF

@csrf_exempt
def relay_control_view(request):
    global relay_state

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            relay_state_input = data.get('relay_state', None)

            if relay_state_input is not None:
                # Update relay state based on input
                if relay_state_input == "true":
                    relay_state = True
                    # Add code here to physically turn the relay ON
                    return JsonResponse({'message': 'Relay turned ON', 'relay_state': 'true'}, status=200)
                elif relay_state_input == "false":
                    relay_state = False
                    # Add code here to physically turn the relay OFF
                    return JsonResponse({'message': 'Relay turned OFF', 'relay_state': 'false'}, status=200)
                else:
                    return JsonResponse({'error': 'Invalid relay state'}, status=400)
            else:
                return JsonResponse({'error': 'No relay state provided'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    elif request.method == 'GET':
        # Return the current relay state
        return JsonResponse({'relay_state': 'true' if relay_state else 'false'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_relay_status(request):
    """
    This view returns the current relay status in JSON format.
    It responds with either "true" or "false" depending on the state.
    """
    global relay_state

    # Return relay status as JSON
    return JsonResponse({'relay_state': relay_state})