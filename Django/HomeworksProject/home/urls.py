# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 19:08:36 2020

@author: stvyh
"""

from django.conf.urls import url
from home.views import HomeView, change_friends

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$',
        change_friends,name='change_friends')

] 