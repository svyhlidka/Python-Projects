# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 20:34:43 2020

@author: stvyh
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import UserProfile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    
    class Meta:
        model = User
        # must define fields you want from to work with
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2')
        
    def safe(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        #befor commit we want validity check first
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        user.email      = self.cleaned_data['email']
        
        if commit:
            user.save()
            
        return User
    
    
class EditProfileForm(UserChangeForm):
    
    class Meta:
        model = User
        
        fields = {
            'username',
            'first_name',
            'last_name',
            'email',
             'password'
            }
    
    
class xEditProfileForm(forms.Form):   #UserChangeForm):
    
    class Meta:
        model = UserProfile
        
        fields = {
                'description',
                'addres1',
                'addres2',
                'addres3',
                'city',
                'state',
                'country',
                'zip_code',
                'phone',
                'mobile',
                'webSite',
                'delivery_addres',
                'image'
                  }
    
        fields_order = ['description',
                'addres1',
                'addres2',
                'addres3',
                'city',
                'state',
                'country',
                'zip_code',
                'phone',
                'mobile',
                'webSite',
                'delivery_addres',
                'image' ]

