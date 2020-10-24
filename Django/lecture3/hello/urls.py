# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 16:36:58 2020

@author: stvyh
"""

from django.urls import path
from . import views  #each app has a views.py

urlpatterns = [
    path("",views.index,name="index"),
    path("racoon",views.racoon,name="racoon"),
   # path("<str:name>",views.byName,name="byName"),
    path("<str:name>",views.greet,name="greet")
    ]
