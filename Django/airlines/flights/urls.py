# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 18:42:13 2020

@author: stvyh
"""

from django.urls import path
from . import views  #each app has a views.py

app_name = "flights"

urlpatterns = [
               path("",views.index,name="index"),
              ]