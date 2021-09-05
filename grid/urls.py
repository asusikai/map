from django.urls import path
from .views import *


app_name="grid"
urlpatterns = [
    path('',show,name="show"),
    path('ifr/',ifr,name="ifr"),
    path('hi/',hi,name="hi"),
    path('jq/',testjq,name="testjq"),
    path('check/',check,name="check"),
]