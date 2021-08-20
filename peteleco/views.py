from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
import pandas as pd
from .models import *
# Create your views here.

User = get_user_model()


def login(request):
    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'index.html')
    
@login_required
def teste(request):
	sensor = Sensor.objects.filter(user_id = request.user.id)
	measure = Measure.objects.all()
	alarm = Alarm.objects.all()
	list_id = []
	if len(sensor) != 0:
		for i in sensor:
			list_id.append(i.id)

		df = pd.DataFrame({'Id' : list_id})
		df['Total'] = 0.0
		df['Alarm'] = 0.0

		for i in alarm:
			param = df[df['Id']==i.sensor_alarm_id].index[0]
			df['Alarm'][param] = i.limit

		for i in measure:
			param = df[df['Id']==i.sensor_id].index[0]
			df['Total'][param] = df['Total'][param] + i.value/1000.0

		lst = list(sensor)
		for i in range(0,len(sensor)):
			lst[i].total = float("%.2f" %df['Total'][i])
		for i in range(0,len(sensor)):
			lst[i].alarm = float("%.2f" %df['Alarm'][i])
		totalite = "%.2f" % (sum(df['Total']) * 0.008)
		context = {
	            'sensor':lst,
	            'measure': measure,
	            'alarm': alarm,
	            'totalite': totalite,
	            }
		return render(request, 'dynamic_update.html', context)
	else:
		return render(request, 'dynamic_update.html')