from channels.consumer import SyncConsumer
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from inbox.models import Conversation, Message, MessagePhoto, MessageDelivery, ConversationStatus
from useraccounts.models import User
from django.db import transaction
import base64
from django.core.files.base import ContentFile
from django.db.models import Q
from django.template.loader import render_to_string
from nibedok.ImageManager import getProcessedImage
class Consumer(SyncConsumer):
    
    
    def websocket_connect(self, event):
        self.send({
          'type':'websocket.accept'
        })
        conversations = Conversation.objects.filter(Q(person_one_group=self.scope['user'].channel_group_name) | Q(person_two_group=self.scope['user'].channel_group_name)).order_by('-last_message')
        data = {
            'conversations':conversations[:10],
            'current_user_id':self.scope['user'].id
        }
        html = render_to_string('latest-conversations.html',data)
        conv_status_count = ConversationStatus.objects.filter(conversation_id__in=conversations,last_receiver_id=self.scope['user'].id,has_unread_msg=True).count()
        response = {
            'status':'connected',
            'extra_message':'test',
            'unread_msg_count':conv_status_count,
            'html':html
        }
        self.send({
          'type':'websocket.send',
          'text':json.dumps(response)  
        })

        
    def websocket_receive(self, event):
        client_data = json.loads(event['text'])
        print(client_data)
        task=client_data['task']
        if task=='add_group':
            async_to_sync(self.channel_layer.group_add)(
                self.scope['user'].channel_group_name, self.channel_name
            )
        elif task=='send_msg':
            text=client_data.get('text')
            sender=self.scope['user'].id
            receiver=client_data.get('receiver')
            sender_group=self.scope['user'].channel_group_name
            receiver_group=client_data.get('receiver_group')
            with transaction.atomic():
                conversation_exists = Conversation.objects.filter(Q(person_one_group=sender_group,person_two_group=receiver_group) | Q(person_one_group=receiver_group,person_two_group=sender_group)).exists()
                if conversation_exists:
                    conversation = Conversation.objects.get(Q(person_one_group=sender_group,person_two_group=receiver_group) | Q(person_one_group=receiver_group,person_two_group=sender_group))
                else:
                    conversation = Conversation.objects.create(person_one_group=sender_group,person_two_group=receiver_group)
                conversation.save()
                conv_status_exists = ConversationStatus.objects.filter(conversation_id=conversation.id).exists()
                if conv_status_exists:
                    conv_status = ConversationStatus.objects.get(conversation_id=conversation.id)
                    conv_status.last_receiver_id = receiver
                    conv_status.has_unread_msg = True
                else:
                    conv_status = ConversationStatus.objects.create(conversation_id=conversation.id,last_receiver_id=receiver,has_unread_msg=True)
                conv_status.save()
                message=Message.objects.create(conversation=conversation,sender=sender,receiver=receiver,sender_group=sender_group,receiver_group=receiver_group,text=text)
                msg_list = []
                for image_b64 in client_data.get('msg_img'):
                    format, imgstr = image_b64.split(';base64,')
                    ext = format.split('/')[-1]
                    msg_img = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                    msg_img = getProcessedImage(msg_img)
                    msg_list.append(MessagePhoto(message=message,photo=msg_img))
                MessagePhoto.objects.bulk_create(msg_list)
                msg_img_arr = []
                for photo in message.photos():
                    msg_img_arr.append(photo.photo)
                self.send({
                    'type':'websocket.send',
                    'text':json.dumps({'status':'sent','msg_img_arr':msg_img_arr,'sent_at':message.created_at,'msg_serial':client_data.get('msg_serial'),'msg_id':message.id},default=str)
                })
                MessageDelivery.objects.create(message=message)
        # elif task=='report_delivery':
        #     msg_id=client_data.get('msg_id')
        #     receiver_group=client_data.get('receiver_group')
        #     msg_delivery=MessageDelivery.objects.get(message_id=msg_id)
        #     msg_delivery.delivered_at=client_data.get('delivered_at')
        #     msg_delivery.if_delivered=True
        #     msg_delivery.save()
        #     data={
        #         'status':'delivered',
        #         'msg_id':msg_id,
        #         'delivered_at':client_data.get('delivered_at')
        #     }
        #     async_to_sync(self.channel_layer.group_send)(
        #         receiver_group,{
        #             'type':'report_delivery',
        #             'text':json.dumps(data,default=str)
        #         }
        #     )
        elif task=='load_prev_msg':
            first_msg_id = client_data.get('first_msg_id')
            sender_channel_group = client_data.get('sender_group')
            receiver_channel_group = client_data.get('receiver_group')
            current_user_id = int(client_data.get('current_user_id'))
            current_user_name = client_data.get('current_user_name')
            other_user_id = int(client_data.get('other_user_id'))
            other_user_name = client_data.get('other_user_name')
            messages = reversed(Message.objects.filter(Q(id__lt=first_msg_id,sender_group=sender_channel_group,receiver_group=receiver_channel_group) | Q(id__lt=first_msg_id,sender_group=receiver_channel_group,receiver_group=sender_channel_group)).order_by('-id')[:3])
            data = {
                'messages':messages,
                'current_user_id':current_user_id,
                'current_user_name':current_user_name,
                'other_user_id':other_user_id,
                'other_user_name':other_user_name,
            }
            print(data)
            html = render_to_string('prev-messages.html',data)
            print(html)
            self.send({
                'type':'websocket.send',
                'text':json.dumps({'status':'got_prev_msg','html':html})
            })
        elif task=='load_older_conv':
            curr_conv_length = client_data.get('curr_conv_length')
            target_length = curr_conv_length+2
            conversations = Conversation.objects.filter(Q(person_one_group=self.scope['user'].channel_group_name) | Q(person_two_group=self.scope['user'].channel_group_name)).order_by('-last_message')[curr_conv_length:target_length]
            print(len(conversations))
            data = {}
            data['status'] = 'got_older_conv'
            data['conversations'] = {}
            for conversation in conversations:
                if conversation.person_one_group == self.scope['user'].channel_group_name:
                    data['conversations'][conversation.person_two_group] = {}
                    data['conversations'][conversation.person_two_group]['last_message'] = conversation.last_message
                    if conversation.lastMessage().sender == self.scope['user'].id:
                        data['conversations'][conversation.person_two_group]['name'] = conversation.lastMessage().receiverInfo().first_name+' '+conversation.lastMessage().receiverInfo().last_name
                        if conversation.lastMessage().photos():
                            data['conversations'][conversation.person_two_group]['lastMessage'] = "You: <i>Photo(s)</i>"
                        else:
                            data['conversations'][conversation.person_two_group]['lastMessage'] = "You: "+conversation.lastMessage().text
                        data['conversations'][conversation.person_two_group]['conv_status'] = False
                    else:
                        data['conversations'][conversation.person_two_group]['name'] = conversation.lastMessage().senderInfo().first_name+' '+conversation.lastMessage().senderInfo().last_name
                        data['conversations'][conversation.person_two_group]['lastMessage'] = conversation.lastMessage().text
                        data['conversations'][conversation.person_two_group]['conv_status'] = conversation.convStatus().has_unread_msg
                else:
                    data['conversations'][conversation.person_one_group] = {}
                    data['conversations'][conversation.person_one_group]['last_message'] = conversation.last_message
                    if conversation.lastMessage().sender == self.scope['user'].id:
                        data['conversations'][conversation.person_one_group]['name'] = conversation.lastMessage().receiverInfo().first_name+' '+conversation.lastMessage().receiverInfo().last_name
                        if conversation.lastMessage().photos()>0:
                            data['conversations'][conversation.person_one_group]['lastMessage'] = "You: <i>Photo(s)</i>"
                        else:
                            data['conversations'][conversation.person_one_group]['lastMessage'] = "You: "+conversation.lastMessage().text
                        data['conversations'][conversation.person_one_group]['conv_status'] = False
                    else:
                        data['conversations'][conversation.person_one_group]['name'] = conversation.lastMessage().senderInfo().first_name+' '+conversation.lastMessage().senderInfo().last_name
                        data['conversations'][conversation.person_one_group]['lastMessage'] = conversation.lastMessage().text
                        data['conversations'][conversation.person_one_group]['conv_status'] = conversation.convStatus().has_unread_msg
            print(json.dumps(data,default=str))
            self.send({
                'type':'websocket.send',
                'text':json.dumps(data, default=str)
            })


    def message_send(self,event):
        data = json.loads(event.get('data'))
        print(data)
        self.send({
            'type':'websocket.send',
            'text':json.dumps(data)
        })
        

    def report_delivery(self,event):
        data = json.loads(event.get('text'))
        self.send({
            'type':'websocket.send',
            'text':json.dumps(data,default=str)
        })