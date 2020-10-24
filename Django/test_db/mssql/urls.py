# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 22:07:06 2020

@author: stvyh
"""
from django.urls import path
from . import views  #each app has a views.py

app_name = "mssql"

urlpatterns = [
               path("",views.index,name="index"),
               path("new_airport/",views.new_airport, name="new_airport"),
               path("new_flight/",views.new_flight, name="new_flight"),
               path("<int:flight_id>",views.flight_by_id, name="flight_by_id"),
               path("<int:flight_id>/book",views.book, name="book"),
              ]