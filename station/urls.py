from django.urls import path
from . import views
urlpatterns = [
    path('add_station/', views.Add_station, name='addStation'),
]