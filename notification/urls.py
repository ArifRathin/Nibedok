from django.urls import path
from .views import allNotifications

urlpatterns = [
    path('all-notifications',allNotifications,name='all-notifications')
]