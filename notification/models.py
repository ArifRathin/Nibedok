from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from useraccounts.models import User
import json
from django.urls import reverse
# Create your models here.
class NotificationType(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Notification(models.Model):
    notif_for = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    post_id = models.BigIntegerField(default=None, null=True)
    post_code_name = models.CharField(default=None, null=True, max_length=250)
    notif_msg = models.CharField(max_length=250, default=None, null=True)
    total_offers = models.BigIntegerField(default=0)
    if_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Notification)
def save(sender, instance, **kwargs):
    if instance.if_read is False:
        group_name = instance.notif_for.channel_group_name
        data={
            'status':'updated_notif',
            'id':instance.id,
            'msg':instance.notif_msg,
            'url':reverse('my-post-wise-offers',kwargs={'post_code_name':instance.post_code_name})
    
        }
        async_to_sync(get_channel_layer().group_send)(
            group_name, {'type':'send_notification','text':json.dumps(data, default=str)}
        )