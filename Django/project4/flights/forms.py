# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 15:11:54 2020

@author: stvyh
"""

from django import forms

from .models import Airports

class AirportForm(forms.ModelForm):

    class Meta:
        model = Airports
        fields = ('airport_id', 'city',)