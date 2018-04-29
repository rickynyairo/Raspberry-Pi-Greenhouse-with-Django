#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep
import Adafruit_DHT
from django.utils import timezone
from models import SensorData
#Pin Setup
#ldr == light dependant resistor
ldr=24
fan_forward = 20
soil_moisture = 21
water_pump = 16
vent_servo = 2
vent_angle = 90
dht_pin = 19

#GPIO SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setup(fan_forward, GPIO.OUT)
GPIO.setup(water_pump, GPIO.OUT)
GPIO.setup(soil_moisture, GPIO.IN)
GPIO.setup(vent_servo, GPIO.OUT)



class GreenhouseSystem(object):
	sensor=Adafruit_DHT.DHT11
	soil_moisture_state = GPIO.input(soil_moisture)

	def get_soil_moisture(self):
		if self.soil_moisture_state == 1:
			state='wet'
		else:
			state='dry'
		return state

	def get_temperature(self):
		humidity, temperature = Adafruit_DHT.read_retry(
			sensor=self.sensor,
			pin = dht_pin,
			retries=5
		)
		return temperature

	def get_humidity(self):
		humidity, temperature = Adafruit_DHT.read_retry(
			sensor=self.sensor,
			pin = dht_pin,
			retries=5
		)
		return humidity

	def ldr_reading(self):
		count=0

		GPIO.setup(ldr, GPIO.OUT)
		GPIO.output(ldr, GPIO.LOW)
		time.sleep(1)

		GPIO.setup(ldr,GPIO.IN)

		while(GPIO.input(ldr)==GPIO.LOW):
			count += 1

		return count

	def open_vent(self, angle = vent_angle):
		#setup pwm on servo pin
		pwm = GPIO.PWM(vent_servo, 50)
		
		#start with 0 duty cycle
		pwm.start(0)

		#Calculate duty cycle
		duty = (angle / 18) + 2
		GPIO.output(vent_servo, True)

		pwm.ChangeDutyCycle(duty)
		sleep(1)

		GPIO.output(vent_servo, False)
		pwm.ChangeDutyCycle(0)

	def record_sensor_values(self):
        #Save sensor readings to database
		db_table=SensorData()
		db_table.temperature = float(self.get_temperature())
		db_table.humidity = float(self.get_humidity())
		db_table.soil_moisture_state = self.get_soil_moisture()
		db_table.date_recorded = timezone.now()
		db_table.save()


