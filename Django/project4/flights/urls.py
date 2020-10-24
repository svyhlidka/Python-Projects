# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 22:39:29 2020

@author: stvyh
"""


from django.urls import path
from . import views  #each app has a views.py

app_name = "flights"

urlpatterns = [
    path("",views.index, name="index"),
    path("new_airport/",views.new_airport, name="new_airport"),
    ]