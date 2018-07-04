#standard imports
import json
import datetime

#django imports
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User

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

@csrf_exempt
def commands(request):
	command_id = int(request.POST['command'])
	user = User.objects.get(username=request.user.username)
	#command_id = json.loads(request.body.decode("utf-8"))['command']
	greenhouse = GreenHouse()
	if command_id == 100:
		greenhouse.switch_lights("off")
		act = ActivityMeta("lights_off", user)
		response = JsonResponse({"lights":"off"}, status=201)
	elif command_id == 101:
		greenhouse.switch_lights("on")
		#act = ActivityMeta("lights_on", user)
		response = JsonResponse({"lights":"on"}, status=201)
	elif command_id == 200:
		greenhouse.move_vent(80)
		#act = ActivityMeta("open_vent", user)
		response = JsonResponse({"vent":"open"}, status=201)
	elif command_id == 201:
		greenhouse.move_vent(10)
		#act = ActivityMeta("close_vent", user)
		response = JsonResponse({"vent":"closed"}, status=201)
	elif command_id == 300:
		greenhouse.switch_pump(3)
		#act = ActivityMeta("water_crops", user)
		response = JsonResponse({"water pump":"done"}, status=201)
	elif command_id == 400:
		greenhouse.switch_fan("off")
		#act = ActivityMeta("stop_fan", user)
		response = JsonResponse({"fan":"off"}, status=201)
	elif command_id == 401:
		greenhouse.switch_fan("on")
		#act = ActivityMeta("start_fan", user)
		response = JsonResponse({"fan":"on"}, status=201)
	else:
		response = JsonResponse({"error":"command " + str(command_id) + " not found"}, status=400)
	if act:
		act.save()
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

@csrf_exempt
def save_activity(request):
	data = json.loads(request.body.decode("utf-8"))
	serializer = ActivityMetaSerializer(data=data)
	#fields = ('activity','user', 'date_recorded')
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