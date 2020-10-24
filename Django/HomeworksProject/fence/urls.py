# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 21:36:03 2020

@author: stvyh
"""

from django.conf.urls import url
from fence.views import FenceDefinitionView


urlpatterns = [
    url(r'^$', FenceDefinitionView.as_view(), name='fence'),
    
    ]