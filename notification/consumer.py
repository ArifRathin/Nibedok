from channels.consumer import SyncConsumer
import json
from .models import Notification
from django.urls import reverse
from asgiref.sync import async_to_sync

class NotifInboxConsumer(SyncConsumer):


    def websocket_connect(self, event):
        self.send({
            'type':'websocket.accept'
        })

        data={
            'status':'connected'
        }

        self.send({
            'type':'websocket.send',
            'text':json.dumps(data)
        })


    def websocket_receive(self, event):
        sent_msg = json.loads(event.get('text'))
        print(sent_msg['task'])
        task = sent_msg['task']
        if task=='send_notification':
            print("Adddd")
            notifications = Notification.objects.filter(notif_for=self.scope['user'].id).order_by('-updated_at')[:10]
            notification_count = Notification.objects.filter(notif_for=self.scope['user'].id, if_read=False).count()
            msg_details = []
            for notif in notifications:
                if notif.type.name == 'got_offer':
                    tmp = {}
                    tmp['url'] = reverse('my-post-wise-offers',kwargs={'post_code_name':notif.post_code_name})
                    tmp['id'] = notif.id
                    tmp['msg'] = notif.notif_msg
                    msg_details.append(tmp)
            data = {
                'status':'sent_notification',
                'notif_count':notification_count,
                'msg_details':msg_details
            }
            self.send({
                'type':'websocket.send',
                'text':json.dumps(data)
            })
        elif task=='add_group':
            (async_to_sync)(self.channel_layer.group_add)(
                self.scope['user'].channel_group_name,self.channel_name
            )
        elif task=='update_notif_read':
            notification = Notification.objects.filter(notif_for=self.scope['user'].id).update(if_read=True)
            data={
                'status':'notif_read_updated'
            }
            self.send({
                'type':'websocket.send',
                'text':json.dumps(data)
            })


    def websocket_disconnect(self,event):
        print('disconnected')


    def send_notification(self, event):
        notif_msg = json.loads(event.get('text'))
        self.send({
            'type':'websocket.send',
            'text':json.dumps(notif_msg)
        })