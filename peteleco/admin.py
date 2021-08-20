from django.contrib import admin
from .models import *

# Register your models here.

class MeasureInline(admin.StackedInline):
	model = Measure
class AlarmInline(admin.StackedInline):
	model = Alarm
class AlarmAdmin(admin.ModelAdmin):
	model = Alarm
class SensorAdmin(admin.ModelAdmin):
	inlines = (AlarmInline,MeasureInline,)
class MeasureAdmin(admin.ModelAdmin):
	model = Measure

admin.site.register(Sensor, SensorAdmin)
admin.site.register(Alarm, AlarmAdmin)
admin.site.register(Measure, MeasureAdmin)