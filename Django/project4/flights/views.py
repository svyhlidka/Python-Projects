from django import forms  #new
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from flights.models import *
from django.db import connections
from .forms import AirportForm



# Create your views here.

 
def index(request):
#    if "flights" not in request.session:
#        request.session["flights"] = []
    sql = connections['default'].cursor()
    sql.execute('select * from airports')
 #   data = dict(sql.fetchall())
    all_posts = Airports.objects.all()
  #  print(data)
    return render(request, 'flights/index.html',  {'all_posts': all_posts})      
  
#    return render(request, 'flights/index.html', {
#             "Flights": request.session["result"]
#        })
                                        
                                        
def new_airport(request):
    if request.method == "POST":
        form = AirportForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.author = request.user
            #post.published_date = timezone.now()
            post.save()

            return redirect('index', pk=Airport.pk)
            #HttpResponseRedirect(reverse('flights:index'))
    else:
        form = AirportForm()
    return render(request, 'flights/new_airport.html',{'form': form})