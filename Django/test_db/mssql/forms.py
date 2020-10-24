# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 20:08:52 2020

@author: stvyh
"""

from django import forms

from .models import *

class AirportForm(forms.ModelForm):

    class Meta:
        model = Airports
        fields = ('airport', 'city',)
        
        
class FlightForm(forms.ModelForm):

    class Meta:
        model = Flights
        fields = ('departure', 'arrival','duration')
        
        