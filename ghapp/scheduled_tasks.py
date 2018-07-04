import requests

from GHMCS_OO import GreenhouseSystem as GreenHouse


def main():
	gh = GreenHouse()

	temperature = gh.get_temperature()
	humidity = gh.get_humidity()
	soil_moisture_state = gh.get_soil_moisture()

	#corrective actions such as watering or airing based on conditions in the greenhouse
	if temperature > 26:
		gh.switch_fan("on")
	elif humidity > 70:
		gh.move_vent(90)
		gh.switch_fan("off")
	elif soil_moisture_state == "dry":
		gh.switch_pump()
	

	url = "http://raspi/ghapp/save_data/"
	data = {
		"temperature":temperature,
		"humidity":humidity,
		"soil_moisture_state":soil_moisture_state
	}
	
	#save data to db via the server:
	r = requests.post(url=url, json=data)

	print (r.text)


if __name__ == "__main__":
	main()
