from django.conf.urls import url, include
from django.contrib import admin


from .views import food, home

urlpatterns = [
    url(r'^food$', food, name='food'),
    url(r'^home$', home, name='home')
]
