import os
import time
from httplib2 import Http
import wiringpi2

io = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_PINS)
io.pinMode(21, io.OUTPUT)

from urllib import urlencode

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

while True:
        temp = read_temp()
        print ("Temperatura:" + str(temp))
        h = Http()
        data = dict(key="S60LM7M7WUKN2HM4",field1=str(temp))
        content = h.request('https://api.thingspeak.com/update', "POST", urlencode(data))
        if (temp >=18):
	    print("if temp" + str(temp))
            io.digitalWrite(21, io.LOW)
        time.sleep(30)
