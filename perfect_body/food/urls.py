from django.conf.urls import url

from .views import *


urlpatterns = [
    url(r'^food$', food, name='food'),
    url(r'^home$', home, name='home'),
    url(r'^profile$', profile, name='profile'),
    url(r'^login$', login, name='login'),
    url(r'^registration$', registration, name='registration'),
    url(r'^logout$', logout, name='logout'),
    url(r'^change_password$', changePassword, name='change_password'),
    url(r'^change_data$', changeData, name='change_data'),
    url(r'^breakfast$', breakfast, name='Breakfast'),
    # url(r'^lunch$', lunch, name='lunch'),
    # url(r'^dinner$', dinner, name='dinner'),
]
