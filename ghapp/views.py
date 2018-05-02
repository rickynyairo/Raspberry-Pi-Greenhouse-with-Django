from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
#from res_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
import datetime

from .serializers import SensorDataSerializer
from .models import SensorData, ActivityMeta
from .GHMCS_OO import GreenhouseSystem as GreenHouse


def index(request):
	return render(request, 'ghapp/index.html')


def control_panel(request):
	pass

def system_preview(request):
	if request.user.is_authenticated:
		greenhouse = GreenHouse()
		activities_qs = list(ActivityMeta.objects.all())[:3]
		context = {
			'temperature':str(greenhouse.get_temperature()),
			'humidity':str(greenhouse.get_humidity()),
			'soil_moisture':str(greenhouse.get_soil_moisture()),
			'activities':activities_qs
		}
		rendered = render(request, 'ghapp/system_preview.html', context=context)
	else:
		rendered = render(request, 'ghapp/index.html')
	return rendered


@csrf_exempt
def save_data(request):
	data = request.json
	'''data2 = {
		"temperature":666,
		"humidity":777,
		"soil_moisture_state":"wet"	
	}'''
	serializer = SensorDataSerializer(data=data)

	if serializer.is_valid():
		serializer.save()
		return JsonResponse(serializer.data, status=201)
	else:
		return JsonResponse(serializer.errors, status=400)


"""
	if request.user.is_authenticated:
		sensor_qs = list(SensorData.objects.get())[0]
		activities_qs = list(ActivityMeta.objects.all())[:3]
		context = {
			'temperature':str(sensor_qs.temperature),
			'humidity':str(sensor_qs.humidity),
			'soil_moisture':str(sensor_qs.get_soil_moisture_state_display()),
			'activities':activities_qs
		}
		rendered = render(request, 'ghapp/system_preview.html', context=context)
	else:
		rendered = render(request, 'ghapp/index.html')
	return rendered
"""