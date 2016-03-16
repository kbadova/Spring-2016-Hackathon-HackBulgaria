from django.conf.urls import url

from .views import registration, home, login

urlpatterns = [
    url(r'^home$', home, name='home'),
    url(r'^registration$', registration, name='registration'),
    url(r'^login$', login, name='login'),
]
