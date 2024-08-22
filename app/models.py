from django.db import models

class TemperatureHumidity(models.Model):
    temperature = models.CharField(max_length=20)
    humidity = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Temperature: {self.temperature} °C, Humidity: {self.humidity} %"
