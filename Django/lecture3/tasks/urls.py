# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 12:27:38 2020

@author: stvyh
"""

from django.urls import path
from . import views  #each app has a views.py

app_name = "tasks"

urlpatterns = [
    path("",views.index, name="index"),
    path("add",views.add, name="add")
    ]