from django.urls import path
from .views import conversation

urlpatterns = [
    path('conversation/<str:name>', conversation, name='conversation')
]