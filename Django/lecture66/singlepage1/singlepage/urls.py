# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 17:18:19 2020

@author: stvyh
"""

from django.urls import path
from . import views  #each app has a views.py

app_name = "sections"

urlpatterns = [
               path("",views.index,name="index"),
               path("sections/<int:num>",views.section, name="section"),
              ]
