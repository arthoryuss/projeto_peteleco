from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from peteleco.models import *
from django.core.mail import send_mail
from django.conf import settings

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        trat1 = ''
        trat2 = ''

        for i in range(0,len(message)):
            if message[i] == ',':
                trat2 += str(message[i+1])
                break
            else:
                trat1 += message[i]

        # Send message to room group
        measure = Measure(sensor_id=int(trat2), value=float(trat1))
        measure.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'total': trat1,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        alarme = 9999
        trat1 = ''
        trat2 = ''
        for i in range(0,len(message)):
            if message[i] == ',':
                trat2 += str(message[i+1])
                break
            else:
                trat1 += message[i]

        list_measure = Measure.objects.filter(sensor_id=int(trat2))
        measure_total = Measure.objects.all()
        list_alarm = Alarm.objects.filter(sensor_alarm_id=int(trat2))
        list_total = []
        totalite = 0

        for i in measure_total:
            totalite = totalite + i.value

        for i in list_measure:
            list_total.append(i.value)
        total = sum(list_total)/1000
        for i in list_alarm:
            if i.limit < total and i.send_email == False:
                subject = 'TESTE ALARME'
                menssagem = ' Apenas um teste de alarme '
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['arthur_bertuleza@hotmail.com',]
                send_mail( subject, menssagem, email_from, recipient_list )
                i.send_email = True
                i.save()
        for i in list_alarm:
            alarme = i.limit
        # Send message to WebSocket
        if alarme != 9999:
            self.send(text_data=json.dumps({
                'total': total,
                'rash' : trat2,
                'message' : message,
                'alarm' : alarme,
                'totalite': (totalite/1000)*0.008,
            }))
        else: 
            self.send(text_data=json.dumps({
                'total': total,
                'rash' : trat2,
                'message' : message,
                'totalite' : (totalite/1000)*0.008,
            }))
