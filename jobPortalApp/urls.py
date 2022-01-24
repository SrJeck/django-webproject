from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('creatt/', views.index),
]

# benitez
# for job seeker profile
urlpatterns += [
    path('seeker-info/', views.seeker_no_info, name="seeker_no_info"),
]
