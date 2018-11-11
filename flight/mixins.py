from django.db import models
from django.utils.translation import ugettext_lazy as _


class FlightMixin(models.Model):
    arrival_location = models.CharField(max_length=255, blank=False, null=True)
    departure_location = models.CharField(max_length=255, blank=False, null=True)
    arrival_time = models.TimeField(_(u"Arrival Time"), blank=False, null=True)
    arrival_date = models.DateField(_(u"Arrival Date"), blank=True, null=True)
    departure_date = models.DateField(_(u"Departure Date"), blank=True, null=True)
    departure_time = models.TimeField(_(u"Departure Time"), blank=False, null=True)

    class Meta:
        abstract = True
