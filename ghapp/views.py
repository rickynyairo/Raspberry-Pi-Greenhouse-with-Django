#standard imports
import json
import datetime

#django imports
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone

#relative imports
from .serializers import SensorDataSerializer, ActivityMetaSerializer
from .models import SensorData, ActivityMeta
from .GHMCS_OO import GreenhouseSystem as GreenHouse


def index(request):
	return render(request, 'ghapp/index.html')

def control_panel(request):
	if request.user.is_authenticated:
		rendered = render(request, 'ghapp/control_panel.html')
	else:
		rendered = render(request, 'ghapp/index.html')
	return rendered

def system_preview(request):
	if request.user.is_authenticated:
		greenhouse = GreenHouse()
		light_intensity = greenhouse.ldr_reading()
		activities_qs = list(ActivityMeta.objects.all())[:4]
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

def analytics(request):
	if request.user.is_authenticated:
		data = list(SensorData.objects.all())[:20]
		temperature = []
		humidity = []

		for data_object in data:
			temperature.append(float(data_object.temperature))
			humidity.append(float(data_object.humidity))
		
		context = {
			"temperature":temperature,
			"humidity":humidity
		}
		
		rendered = render(request, "ghapp/analytics.html", context=context)
	else:
		rendered = render(request, 'ghapp/index.html')
	return rendered

@csrf_exempt
def commands(request):
	command_id = int(request.POST['command'])
	greenhouse = GreenHouse()
	if command_id == 100:
		greenhouse.switch_lights("off")
		response = JsonResponse({"lights":"off"}, status=201)
	elif command_id == 101:
		greenhouse.switch_lights("on")
		response = JsonResponse({"lights":"on"}, status=201)
	elif command_id == 200:
		greenhouse.move_vent(80)
		response = JsonResponse({"vent":"open"}, status=201)
	elif command_id == 201:
		greenhouse.move_vent(170)
		response = JsonResponse({"vent":"closed"}, status=201)
	elif command_id == 300:
		if greenhouse.get_soil_moisture() == "wet":
			response = JsonResponse({"water pump":"the soil is wet"}, status=201)
		else:
			greenhouse.switch_pump(3)
			response = JsonResponse({"water pump":"done"}, status=201)
	elif command_id == 400:
		greenhouse.switch_fan("off")
		response = JsonResponse({"fan":"off"}, status=201)
	elif command_id == 401:
		greenhouse.switch_fan("on")
		response = JsonResponse({"fan":"on"}, status=201)
	else:
		response = JsonResponse({"error":"command " + str(command_id) + " not found"}, status=400)
	return response

@csrf_exempt
def save_data(request):
	data = json.loads(request.body.decode("utf-8"))
	serializer = SensorDataSerializer(data=data)

	if serializer.is_valid():
		serializer.save()
		return JsonResponse(serializer.data, status=201)
	else:
		return JsonResponse(serializer.errors, status=400)