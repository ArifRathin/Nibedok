from django.shortcuts import render
from useraccounts.models import User
from .models import Conversation
from django.db.models import Q
# Create your views here.
def conversation(request, name):
    conversations = Conversation.objects.filter(Q(person_one_group=request.user.channel_group_name) | Q(person_two_group=request.user.channel_group_name)).order_by('-last_message')[:2]
    conversation = None
    if name == 'all_msgs':
        data={
            'user':None,
            'conversations':conversations,
            'conversation':conversation,
            'env':'message_room',
            'name':name
        }
        return render(request,'message-system.html',data)
    user = User.objects.get(channel_group_name=name)
    conversation_exists = Conversation.objects.filter(Q(person_one_group=request.user.channel_group_name,person_two_group=user.channel_group_name) | Q(person_two_group=request.user.channel_group_name,person_one_group=user.channel_group_name)).exists()
    if conversation_exists:
        conversation = Conversation.objects.get(Q(person_one_group=request.user.channel_group_name,person_two_group=user.channel_group_name) | Q(person_two_group=request.user.channel_group_name,person_one_group=user.channel_group_name))
        status = conversation.convStatus()
        status.has_unread_msg = False
        status.save()
    data={
        'user':user,
        'conversations':conversations,
        'conversation':conversation,
        'env':'message_room',
        'name':name
    }
    return render(request,'message-system.html',data)
    return render(request,'message-room.html',data)
    return render(request,'conversation.html',data)