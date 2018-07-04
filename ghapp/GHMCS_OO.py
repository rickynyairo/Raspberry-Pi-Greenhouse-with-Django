#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep
import Adafruit_DHT

ldr = 16
led = 22
fan = 12
soil_moisture = 21
water_pump = 4
vent_servo = 2
vent_angle = 90
dht_pin = 20


#GPIO SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setup(fan, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(water_pump, GPIO.OUT)
GPIO.setup(soil_moisture, GPIO.IN)
GPIO.setup(vent_servo, GPIO.OUT)



class GreenhouseSystem(object):
	def get_soil_moisture(self):
		if GPIO.input(soil_moisture) == 0:
			state='wet'
		else:
			state='dry'
		return state

	def switch_lights(self, state='on'):
		if state is 'on':
			GPIO.output(led, GPIO.HIGH)
		elif state is 'off':
			GPIO.output(led, GPIO.LOW)
		else:
			GPIO.output(led, GPIO.LOW)

	def switch_fan(self, state='on'):
		if state is 'on':
			GPIO.output(fan, GPIO.HIGH)
		elif state is 'off':
			GPIO.output(fan, GPIO.LOW)
		else:
			GPIO.output(fan, GPIO.LOW)

	def get_temperature(self):
		humidity, temperature = Adafruit_DHT.read_retry(
			sensor=Adafruit_DHT.DHT11,
			pin = dht_pin,
			retries=3
		)
		if temperature is None:
			temperature = 0
			humidity = 0
		return float(temperature)

	def get_humidity(self):
		humidity, temperature = Adafruit_DHT.read_retry(
			sensor=Adafruit_DHT.DHT11,
			pin = dht_pin,
			retries=3
		)
		
		if humidity is None:
			humidity = 0
			temperature = 0
		return float(humidity)

	def ldr_reading(self):
		count=0

		GPIO.setup(ldr, GPIO.OUT)
		GPIO.output(ldr, GPIO.LOW)
		sleep(1)

		GPIO.setup(ldr,GPIO.IN)

		while(GPIO.input(ldr)==GPIO.LOW):
			count += 1

		return count

	def move_vent(self, angle = vent_angle):
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
	
	def switch_pump(self, duration = 5):
		GPIO.output(water_pump, True)
		sleep(duration)
		GPIO.output(water_pump, False)
		return 0
	

