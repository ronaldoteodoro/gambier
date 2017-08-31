from ubidots import ApiClient
import math
import time
import os
import wiringpi

# Create an ApiClient object

api = ApiClient(token='XXXXXXXXXXXXXXXXXX')

# Get a Ubidots Variable

variable = api.get_variable('59a82988c03f97169d3ba971')

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(24, 1)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor = '/sys/bus/w1/devices/28-051673a417ff/w1_slave'

def temp_raw():

    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():

    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()

    temp_output = lines[1].find('t=')

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

while(1):
    temp = read_temp()
    print ("Temperatura:" + str(temp))
    if (temp >= 18):
        wiringpi.pinMode(24, 0)
    else:
        wiringpi.pinMode(24, 1)

    response = variable.save_value({"value": temp})
    print response
    time.sleep(1)