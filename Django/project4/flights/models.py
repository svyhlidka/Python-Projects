from django.db import models
from datetime import timezone


# Create your models here.

class Airports(models.Model):
    airport_id = models.AutoField(primary_key=True)
    airport    = models.CharField(max_length=3)
    city       = models.CharField(max_length=64)
    created    = models.DateTimeField()
    def __str__(self):
        return f'<{self.airport}> - {self.city}'

    class Meta:
        managed = False
        db_table = 'airports'

class Flights(models.Model):
    flight_id = models.AutoField(primary_key=True)
    departure = models.ForeignKey(Airports, on_delete=models.CASCADE, 
                    related_name='departures')
    arrival   = models.ForeignKey(Airports, on_delete=models.CASCADE,
                     related_name='arrivals')
    duration  = models.IntegerField()

    def __str__(self):
        return f' flight {self.flight_id}: {self.departure} to {self.arrival}'

    class Meta:
        managed = False
        db_table = 'flights'


class Bookings(models.Model):
    booking_id  = models.AutoField(primary_key=True)
    flight_id   = models.ForeignKey(Flights, models.DO_NOTHING,db_column='flight_id')
    pax         = models.IntegerField(db_column='PAX')  # Field name made lowercase.
    flight_date = models.DateTimeField()
    status      = models.CharField(max_length=3)
    created     = models.DateTimeField()
    author      = models.CharField(max_length=64) 
    
    def update(self):
        self.published_date = timezone.now()
        self.save()
    
    def __str__(self):
        return f'<{self.booking_id}>: flight {self.flight_id}, PAX {self.pax}'

    class Meta:
        managed = False
        db_table = 'bookings'


