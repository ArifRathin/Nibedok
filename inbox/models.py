from django.db import models
import os
from uuid import uuid4
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from useraccounts.models import User
import json
import datetime
from django.urls import reverse
# Create your models here.
class Conversation(models.Model):
    person_one_group = models.CharField(max_length=250,default=None,null=True)
    person_two_group = models.CharField(max_length=250,default=None,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_message = models.DateTimeField(auto_now=True)

    def latestMessages(self):
        return reversed(self.message_set.filter(conversation_id=self.id).order_by('-id')[:3])
    
    def lastMessage(self):
        return self.message_set.filter(conversation_id=self.id).latest('id')
    
    def convStatus(self):
        return self.conversationstatus_set.get(conversation_id=self.id)


class ConversationStatus(models.Model):
    conversation = models.ForeignKey(Conversation,on_delete=models.CASCADE)
    last_receiver_id = models.BigIntegerField()
    has_unread_msg = models.BooleanField(default=False)


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.BigIntegerField()
    receiver = models.BigIntegerField()
    sender_group = models.CharField(max_length=250,default=None,null=True)
    receiver_group = models.CharField(max_length=250,default=None,null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def photos(self):
        return self.messagephoto_set.filter(message_id=self.id)
    
    def messageDelivery(self):
        return self.messagedelivery_set.get(message_id=self.id)
    
    def senderInfo(self):
        return User.objects.get(channel_group_name=self.sender_group)
    
    def receiverInfo(self):
        return User.objects.get(channel_group_name=self.receiver_group)


def saveMessagePhoto(instance, filename):
    extension = filename.split('.')[-1]
    if instance.pk:
        filename = f'{instance.pk}{uuid4().hex}.{extension}'
    else:
        filename = f'{uuid4().hex}.{extension}'
    
    return os.path.join('message_photos', filename)


class MessagePhoto(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=saveMessagePhoto)


class MessageDelivery(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    dispatched_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(default=None, null=True)
    if_delivered = models.BooleanField(default=False)


@receiver(post_save, sender=MessageDelivery)
def dispatch_msg(sender,instance,**kwargs):
    if instance.if_delivered == False:
        group_name = instance.message.receiver_group
        print(group_name)
        msg_img_arr = []
        if_img_exists = MessagePhoto.objects.filter(message=instance.message).exists()
        if if_img_exists:
            photos = MessagePhoto.objects.filter(message=instance.message)
            for photo in photos:
                msg_img_arr.append(photo.photo)
        data = {
            'status':'msg_received',
            'text':instance.message.text,
            'msg_img_arr':msg_img_arr,
            'msg_id':instance.message.id,
            'sent_at':instance.message.created_at,
            'conversation_id':instance.message.conversation_id,
            'sender_id':instance.message.sender,
            'sender_first_name':instance.message.senderInfo().first_name,
            'sender_last_name':instance.message.senderInfo().last_name,
            'sender_channel_group_name':instance.message.senderInfo().channel_group_name,
            'sender_channel_group_name':instance.message.senderInfo().channel_group_name,
            'sender_url':reverse('conversation',kwargs={'name':instance.message.senderInfo().channel_group_name}),
            'delivered_at':datetime.datetime.now()
        }
        async_to_sync(get_channel_layer().group_send)(
            group_name,{
                'type':'message_send',
                'data':json.dumps(data,default=str)
            }
        )
