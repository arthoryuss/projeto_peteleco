from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

# Create your views here.


def index2(request):
    return render(request, 'index2.html', {})

def room(request, room_name):
	context ={
			'total': 1
	}
	return render(request, 'room.html', context, {'room_name_json': mark_safe(json.dumps(room_name))})

