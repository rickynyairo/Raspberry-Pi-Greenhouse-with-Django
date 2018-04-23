from django.contrib import admin

from .models import SensorData, ActivityMeta

class SensorDataAdmin(admin.ModelAdmin):
	fieldsets = [
		('Sensor Data', {'fields':['temperature', 'humidity', 'soil_moisture_state', 'date_recorded']}),
	]
	list_display = ('temperature', 'humidity', 'soil_moisture_state', 'date_recorded')
	date_hierarchy = 'date_recorded'
	ordering = ['date_recorded']

class ActivityMetaAdmin(admin.ModelAdmin):
	fieldsets = [
		('Activity', {'fields':['activity', 'user', 'date_recorded']}),
	]
	list_display = ('activity', 'user', 'date_recorded')
	date_hierarchy = 'date_recorded'
	ordering = ['date_recorded']

admin.site.register(SensorData, SensorDataAdmin)
admin.site.register(ActivityMeta, ActivityMetaAdmin)