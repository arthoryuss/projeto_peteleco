from django.db import models
from .choices import *
from django.contrib.auth.models import User

# Create your models here.

class Sensor (models.Model):

	user = models.ForeignKey(User, related_name='Cliente', on_delete=models.CASCADE)
	local = models.CharField ('Local', max_length = 50)
	tipo = models.CharField(
			'Tipo do ponto de vazão',
			max_length=25,
			null=True,
			blank=True,
			choices=FLOWTYPE_CHOICES,
		)
	status = models.BooleanField ('Ativo', default=True)


	def __str__(self):
		return self.tipo


class Measure (models.Model):

	sensor = models.ForeignKey(Sensor, related_name='sensor', on_delete=models.CASCADE) 
	value = models.FloatField ('Valor')
	date_creation = models.DateTimeField('Data da Captura', auto_now_add=True)


class Alarm (models.Model):

	sensor_alarm = models.OneToOneField(Sensor, related_name='sensor_alarm', on_delete=models.CASCADE) 
	tipo = models.CharField(
			'Critério',
			max_length=25,
			choices=ALARMTYPE_CHOICES,
		)
	limit = models.FloatField ('Valor Limite')
	date_finish = models.DateField ('Data para término do alarme')
	status= models.BooleanField ('Repetir', default=False)
	send_email= models.BooleanField ('Email enviado', default=False)
	datecreation = models.DateTimeField('Data da Criação', auto_now_add=True)




