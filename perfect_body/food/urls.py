from django.conf.urls import url

from .views import food, home, profile, login, registration, logout


urlpatterns = [
    url(r'^food$', food, name='food'),
    url(r'^home$', home, name='home'),
    url(r'^profile$', profile, name='profile'),
    url(r'^login$', login, name='login'),
    url(r'^registration$', registration, name='registration'),
    url(r'^logout$', logout, name='logout'),
    # url(r'^saveProfile$', saveProfile, name='saveProfile'),
]
