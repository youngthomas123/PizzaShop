from datetime import datetime
from re import T
import time 
import requests
from fhict_cb_01.CustomPymata4 import CustomPymata4
from datetime import datetime
import time
import csv

DHTPIN = 12
LED1 = 4
LED2 = 5

def current_time():
    rightNow = datetime.now()
    time = rightNow.strftime("%I:%M:%S%p")
    time = time.lstrip('0')
    time = time.lower()
    return time

def current_temp():
    global temperature
    humidity, temperature, timestamp = board.dht_read(DHTPIN)
    return temperature

def setup():
    global board
    board = CustomPymata4(com_port = "COM6")
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05)

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

countdown(900)