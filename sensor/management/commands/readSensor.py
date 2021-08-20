import channels.layers
from asgiref.sync import async_to_sync
from django.core.management import BaseCommand
import time
import json
from chat import consumers
from peteleco.models import *
import pyfirmata
import time

#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
    # Show this when the user types help
    help = "Simulates reading sensor and sending over Channel."
    
    # A command must define handle()
    def handle(self, *args, **options):
        channel_layer = channels.layers.get_channel_layer()
        board = pyfirmata.Arduino('/dev/ttyUSB1')
        it = pyfirmata.util.Iterator(board)
        it.start()

        board.digital[13].mode = pyfirmata.INPUT
        board.digital[2].mode = pyfirmata.INPUT
        cont = 0
        cont2 = 0
        x = 0
        sw = board.digital[13].read()
        sw2=  board.digital[2].read()
        while True:
            while x != 100:
                swold = sw
                swold2 = sw2
                sw = board.digital[13].read()
                sw2=  board.digital[2].read()

                if swold != sw and x != 1:
                    cont = cont+1
                if swold2 != sw2 and x != 1:
                    cont2 = cont2+1
                time.sleep(0.01)
                x = x+1

            if cont != 0:
                measure1 = Measure(sensor_id=int(1), value=(cont * 1.59))
                measure1.save()
                async_to_sync(channel_layer.group_send)('chat_1',{
                'type': 'chat_message',
                'message': '%s,1' % str((cont * 1.59))
                })
            if cont2 != 0:
                measure2 = Measure(sensor_id=int(2), value=(cont2 * 1.53))
                measure2.save()
                async_to_sync(channel_layer.group_send)('chat_1',{
                'type': 'chat_message',
                'message': '%s,2' % str((cont2 * 1.53))
                })
            self.stdout.write("Sensor reading...")
            cont = 0
            cont2 = 0
            x = 0