"""Homeworks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from Homeworks.views import login_redirect
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', login_redirect, name='login_redirect'),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
    url(r'^admin/',   admin.site.urls),
    url(r'^fence/',   include(('fence.urls','fence'), namespace='fence')),
    url(r'^home/',    include(('home.urls','home'), namespace='home')),
    url(r'^account/', include(('accounts.urls','accounts'), namespace='accounts')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





#https://github.com/maxg203/Django-Tutorials/tree/master/tutorial

# from django.conf.urls import url, include
# from django.contrib import admin
# from tutorial import views
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     url(r'^$', views.login_redirect, name='login_redirect'),
#     url(r'^admin/', admin.site.urls),
#     url(r'^account/', include('accounts.urls', namespace='accounts')),
#     url(r'^home/', include('home.urls', namespace='home')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)