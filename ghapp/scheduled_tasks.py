import requests
from sys import argv
from GHMCS_OO import GreenhouseSystem as GreenHouse


def main():
	gh = GreenHouse()

	temperature = gh.get_temperature()
	humidity = gh.get_humidity()
	soil_moisture_state = gh.get_soil_moisture()
	#argument passed into argv[1] determines the action to be performed. 
	#This is either data collection [dc]
	#or system maintenance [sm] in the form of corrective actions. 
	#corrective actions such as watering or airing based on conditions in the greenhouse
	if argv[1] == "sm":
		if temperature > 26 or humidity > 68:
			gh.move_vent(80)
			gh.switch_fan("on")
		elif temperature <= 23 or humidity <= 60:
			gh.move_vent(170)
			gh.switch_fan("off")
		elif soil_moisture_state == "dry":
			gh.switch_pump(3)
		else:
			gh.move_vent(0)
			gh.switch_fan("off")
	elif str(argv[1]) == "dc":
		url = "http://raspi/ghapp/save_data/"
		data = {
			"temperature":temperature,
			"humidity":humidity,
			"soil_moisture_state":soil_moisture_state
		}	

		#save data to db via the server:
		r = requests.post(url=url, json=data)
		r = r.text
	else:
		r = "unrecognized or no command"
		
	return r
if __name__ == "__main__":
	main()
