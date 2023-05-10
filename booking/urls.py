from django.contrib import admin
from django.urls import path, include
from booking import views

app_name = 'booking'
urlpatterns = [
    path('', views.index, name='movie_list'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
]