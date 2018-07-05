from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class SensorData(models.Model):
	SOIL_MOISTURE = (
		('wet','Wet'),
		('dry', 'Dry'),
	)
	
	temperature = models.DecimalField(blank=False, null=False, max_digits = 7, decimal_places = 2)
	humidity = models.DecimalField(blank=False, null=False, max_digits = 7, decimal_places = 2)
	soil_moisture_state = models.CharField(max_length = 10, choices  = SOIL_MOISTURE)
	date_recorded = models.DateTimeField('Date Recorded', auto_now=True)

	class Meta:
		ordering = ('-date_recorded',)

	def __str__(self):
		return 'Recorded: ' + str(self.date_recorded)

class ActivityMeta(models.Model):
	ACTIVITY_CHOICES = (
		('open_vent','Open Vent'),
		('close_vent','Close Vent'),
		('lights_on','Lights On'),
		('lights_off','Lights Off'),
		('start_fan','Start Fan'),
		('stop_fan','Stop Fan'),
		('water_crops','Water Crops'),
	)
	activity = models.CharField(
		max_length = 20,
		choices = ACTIVITY_CHOICES
	)
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	date_recorded = models.DateTimeField(default=timezone.now)
	
	class Meta:
		ordering = ('-date_recorded',)
	
	def __str__(self):
		return 'Recorded: ' + str(self.date_recorded) + ' by ' + str(self.user)