from rest_framework import serializers 

from .models import SensorData, ActivityMeta

class SensorDataSerializer(serializers.ModelSerializer):
	"""Meant to map the querysets into JSON DATA"""

	class Meta:
		"""Meta classs to map serializer's fields with the model fields"""
		model = SensorData
		fields = ('temperature','humidity','soil_moisture_state', 'date_recorded')


class ActivityMetaSerializer():

	class Meta:
		model = ActivityMeta
		fields = ('activity','user', 'date_recorded')

