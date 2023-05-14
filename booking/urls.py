from django.contrib import admin
from django.urls import path, include
from booking import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('events/<str:category>/', views.events_list, name='event_list'),
    path('events/<str:category>/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<str:category>/<int:pk>/reviews/new/', views.review_edit, name='review_create'),
    path('events/<str:category>/<int:pk>/reviews/<int:event_pk>/<int:review_pk>/', views.review_edit, name='review_edit'),
    path('ticket-search/', views.ticket_search, name='ticket_search'),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)