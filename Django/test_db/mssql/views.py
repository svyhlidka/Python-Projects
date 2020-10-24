from django import forms  #new
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from mssql.models import *
from django.db import connections
from .forms import *
from django.core.exceptions import ObjectDoesNotExist

#Create your views here.
def index(request):
#    if "mssql" not in request.session:
#        request.session["mssql"] = []
    all_airports = Airports.objects.all()
    all_flights  = Flights.objects.all()
    return render(request, 'mssql/index.html',
                  {'all_airports': all_airports,'all_flights': all_flights} )      
 
def new_airport(request):
    if request.method == "POST":
        form = AirportForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.author = request.user
            #post.published_date = timezone.now()
            post.save()

            #return redirect('mssql:index', pk=Airports.pk)
            return HttpResponseRedirect(reverse('mssql:index'))
    else:
        form = AirportForm()
    return render(request, 'mssql/new_airport.html',{'form': form})

def flight_by_idOld(request, flight_id):
 #   flight = Flight.objects.get(flight_id=flight_id)
 #   or better
    flight = Flights.objects.get(pk=flight_id)
    try:
        # single record
        #passenger = PassengerFlights.objects.get(flight=flight_id)
        # multiple records
        passenger = PassengerFlights.objects.filter(flight=flight_id)
    except ObjectDoesNotExist:
        passenger = {}
    try:
        non_passenger = PassengerFlights.objects.exclude(flight=flight_id).all()
    except ObjectDoesNotExist:
        non_passenger = {}
    return render(request, 'mssql/flight_by_id.html', {
                               'flight':flight,
                               'passenger':passenger,
                               'non_passenger':non_passenger
                                                       })
def flight_by_id(request, flight_id):
 #   flight = Flight.objects.get(flight_id=flight_id)
 #   or better
    flight = Flights.objects.get(pk=flight_id)
    passenger = PassengerFlights.objects.filter(flight=flight_id)
    if passenger is None:
        passenger = {}
    non_passenger = PassengerFlights.objects.exclude(flight=flight_id).all()
    if non_passenger is None:
        non_passenger = {}
    return render(request, 'mssql/flight_by_id.html', {
                               'flight':flight,
                               'passenger':passenger,
                               'non_passenger':non_passenger
                                                       })
def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        # request.POST["passenger"]  -  to get passenger via form
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse('flight_by_id', arg=(flight.flight_id,)))
       
    
    

def new_flight(request):
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.author = request.user
            #post.published_date = timezone.now()
            post.save()

            #return redirect('mssql:index', pk=Airports.pk)
            return HttpResponseRedirect(reverse('mssql:index'))
    else:
        form = FlightForm()
    return render(request, 'mssql/new_flight.html',{'form': form})