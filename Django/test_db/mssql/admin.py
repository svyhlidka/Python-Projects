from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Airports, Flights, Passengers, PassengerFlights

#added
class FlightAdmin(admin.ModelAdmin):
    list_display = ("flight_id", "departure", "arrival", "duration"  )
    
class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)   

class PassengerFlightAdmin(admin.ModelAdmin):
     list_display = ("pf_id", )



admin.site.register(Airports)
#admin.site.register(Flights)
admin.site.register(Flights, FlightAdmin)
admin.site.register(Passengers, PassengerAdmin)
admin.site.register(PassengerFlights)

