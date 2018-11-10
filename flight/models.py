from django.db import models

# Create your models here.

class Flight(models.Model):
    title = models.CharField(max_length=255, blank=False)
    arrival_location = models.CharField(max_length=255, blank=False)
    departure_location = models.CharField(max_length=255, blank=False)
    arrival_time = models.DateTimeField(blank=False)
    departure_time = models.DateTimeField(blank=False)


    
        
