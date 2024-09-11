from django.urls import path
from .views import TemperatureHumidityDetailView,  TemperatureHumidityListView, LatestTemperatureHumidityAPIView, TemperatureHumidityCreateAPIView, TemperatureHumidityCreateAPIView, temperature_monitor, history_view, relay_control_view, get_relay_status

urlpatterns = [
    path('temperatures/', TemperatureHumidityListView.as_view(), name='temperature-list'),
    path('temperatures/<int:pk>/', TemperatureHumidityDetailView.as_view(), name='temperature-detail'),
    path('createtemperatures/', TemperatureHumidityCreateAPIView.as_view(), name='temperature-create'),
    path('api/latest_temperaturehumidity/', LatestTemperatureHumidityAPIView.as_view(), name='latest_temperaturehumidity'),
    path('temperature-monitor/', temperature_monitor, name='temperature-monitor'),
    path('history/', history_view, name='history'),
    path('relay-control/', relay_control_view, name='relay_control'),
    path('getrelaystatus/', get_relay_status, name='get_relay_status'),
]

