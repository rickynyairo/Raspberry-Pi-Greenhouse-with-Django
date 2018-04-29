import requests

from GHMCS_OO import GreenhouseSystem as GreenHouse


def main():
	greenhouse = GreenHouse()

	temperature = greenhouse.get_temperature()
	humidity = greenhouse.get_humidity()
	soil_moisture_state = greenhouse.get_soil_moisture()

	#Here we'll insert corrective actions such as watering or airing

	url = "http://raspi/ghapp/save_data/"
	data = {
		"temperature":temperature,
		"humidity":humidity,
		"soil_moisture_state":soil_moisture_state
	}

	#save data to db via the server:
	r = requests.post(url=url, data=data)

	print (r)



if __name__ == "__main__":
	main()
