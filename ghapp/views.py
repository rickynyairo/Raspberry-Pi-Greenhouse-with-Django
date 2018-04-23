from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import SensorData, ActivityMeta
#from .GHMCS_OO import GreenhouseSystem as GreenHouse

def index(request):
	return render(request, 'ghapp/index.html')

def control_panel(request, command):
	pass

def system_preview(request):
	'''
	greenhouse = GreenHouse()
	context = {
		'temperature':str(greenhouse.get_temperature()),
		'humidity':str(greenhouse.get_humidity()),
		'soil_moisture':str(greenhouse.get_soil_moisture()),
		'activities':activities_qs
	}
	'''
	if request.user.is_authenticated:
		template_to_render = 'ghapp/system_preview.html'
		sensor_qs = list(SensorData.objects.all())[0]
		activities_qs = list(ActivityMeta.objects.all())[:3]
		context = {
			'temperature':str(sensor_qs.temperature),
			'humidity':str(sensor_qs.humidity),
			'soil_moisture':str(sensor_qs.get_soil_moisture_state_display()),
			'activities':activities_qs
		}
	else:
		context={}
		template_to_render = 'ghapp/login.html'
	
	return render(request, template_to_render, context=context)