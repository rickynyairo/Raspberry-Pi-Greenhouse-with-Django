from GHMCS_OO import GreenhouseSystem as GreenHouse
from time import sleep

def main():
    gh = GreenHouse()

    while(True):
        print("Light intensity: {}".format(gh.ldr_reading()))
        sleep(1)

if __name__ == "__main__":
	main()

