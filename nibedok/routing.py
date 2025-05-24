from django.urls import path
from inbox.consumer import Consumer as msg_consumer
from notification.consumer import NotifInboxConsumer as ni_consumer

ws_urlpatterns = [
    path('ws/nibedok-message/', msg_consumer.as_asgi()),
    path('ws/nibedok-notification-inbox/', ni_consumer.as_asgi()),
]