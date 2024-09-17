from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('suggestion/', views.suggestion, name="suggestion"),
    path('ratings/', views.save_rating, name="ratings")
]
