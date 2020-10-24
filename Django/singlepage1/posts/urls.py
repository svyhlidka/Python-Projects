# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 17:18:19 2020

@author: stvyh
"""

from django.urls import path
#from .views import index, posts
from . import views

app_name = "posts"

urlpatterns = [
               
               path("",views.index,name="index"),
               path("posts", views.posts, name="posts"),
              ]
#                path("",views.index,name="index"),
#              path("posts", views.posts, name="posts"),