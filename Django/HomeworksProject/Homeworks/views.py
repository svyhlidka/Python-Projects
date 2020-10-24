# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 20:54:29 2020

@author: stvyh
"""
from django.shortcuts import redirect

def login_redirect(request):
    return redirect('/account/login')
