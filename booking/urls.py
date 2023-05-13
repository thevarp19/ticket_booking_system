from django.contrib import admin
from django.urls import path, include
from booking import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'booking'
urlpatterns = [
    path('', views.index, name='movie_list'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('movie_detail/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('ticket-search/', views.ticket_search, name='ticket_search'),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)