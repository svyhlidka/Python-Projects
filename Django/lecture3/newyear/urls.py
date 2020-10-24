# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 18:55:11 2020

@author: stvyh
"""

from django.urls import path
from . import views  #each app has a views.py

urlpatterns = [
    path("",views.index,name="index")
    ]
