# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 23:14:25 2020

@author: stvyh
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 21:36:03 2020

@author: stvyh
"""

from django.conf.urls import url
from django.urls import reverse_lazy
from . import views 
from django.contrib.auth.views import (
                                  LoginView, 
                                  LogoutView, 
                                  PasswordResetView, 
                                  PasswordResetDoneView,
                                  PasswordResetConfirmView,
                                  PasswordResetCompleteView
                                  )
from django.conf import settings



urlpatterns = [
    url(r'^login/$', 
        LoginView.as_view(
        template_name='accounts/login.html',
        success_url=reverse_lazy('home:home')
        ), name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^profile/$', views.view_profile, name = 'view_profile'),
    url(r'^profile/(?P<pk>\d+)/$', views.view_profile, name = 'view_profile_with_pk'),
    url(r'^profile/edit/$', views.edit_profile, name = 'edit_profile'),
    url(r'^change-password/$', views.change_password, name = 'change_password'),
    
    url(r'^reset-password/$',
        PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        success_url=reverse_lazy('accounts:password_reset_done'),
        email_template_name='accounts/reset_password_email.html'),
        name='reset_password'),
    
    url(r'^reset-password/done/$', 
        PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),    
    
    url(r'reset-password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')),
        name='password_reset_confirm'),
    
    url(r'^reset-password/complete/$', 
        PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html')
        ,name='password_reset_complete'),    
    ]

