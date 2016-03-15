from django.conf.urls import url, include
from django.contrib import admin

from .views import food

urlpatterns = [
    url(r'^food$', food, name='food'),
]
