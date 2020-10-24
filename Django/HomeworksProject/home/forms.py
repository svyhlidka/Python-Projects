# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 15:34:16 2020

@author: stvyh
"""

from django import forms
from home.models import Post

class HomeForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(
           attrs = {
            'class':'form-control',
            'placeholder':'type a post...'
           }
    ))
    
    class Meta:
        model = Post
        fields = ('post',)    #fields is a tuple!!!, we have only one field here
        
    
    