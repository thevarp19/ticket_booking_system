from django.contrib import admin
from django.urls import path, include
from booking import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('main/', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('', views.sign_up, name='register'),
    path('events/<str:category>/', views.events_list, name='event_list'),
    path('events/<str:category>/<int:pk>/', views.event_detail, name='event_detail'),
    path('review_create/<int:event_pk>/', views.review_edit, name='review_create'),
    path('review_edit/<int:event_pk>/<int:review_pk>/', views.review_edit, name='review_edit'),
    path('event-search/', views.event_search, name='event_search'),
    path('profile/', views.profile_page, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('ticket/<int:pk>/', views.purchase_movie, name='purchase_movie'),
    path('validate/', views.validate_purchase, name='validate_purchase'),
    path('purchase_confirm/', views.purchase_confirm, name='purchase_confirm')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
