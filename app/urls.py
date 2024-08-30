from django.urls import path
from .views import TemperatureHumidityDetailView,  TemperatureHumidityListView, LatestTemperatureHumidityAPIView, TemperatureHumidityCreateAPIView, TemperatureHumidityCreateAPIView, temperature_monitor, temperature_humidity_history

urlpatterns = [
    path('temperatures/', TemperatureHumidityListView.as_view(), name='temperature-list'),
    path('temperatures/<int:pk>/', TemperatureHumidityDetailView.as_view(), name='temperature-detail'),
    path('createtemperatures/', TemperatureHumidityCreateAPIView.as_view(), name='temperature-create'),
    path('api/latest_temperaturehumidity/', LatestTemperatureHumidityAPIView.as_view(), name='latest_temperaturehumidity'),
    path('temperature-monitor/', temperature_monitor, name='temperature-monitor'),
    path('history/', temperature_humidity_history, name='temperature-humidity-history'),
]

