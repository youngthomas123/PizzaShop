from datetime import datetime
import time 
import requests
from fhict_cb_01.CustomPymata4 import CustomPymata4
from datetime import datetime
import time
import csv
import time, sys

DHTPIN = 12
RED_LED = 4
GREEN_LED = 5
BUTTON2 = 9
BUTTON1 = 8
BUZZER = 3
BUTTON_PRESSED = 0
t = 900

def current_time():

    """arg: Importing datetime so you can see the current time the from the device that is running the code,
        we also make the time look nice, with the am/pm as well and removing unnecessary.
        return: the time in an nice formatted way."""

    rightNow = datetime.now()
    time = rightNow.strftime("%I:%M:%S%p")
    time = time.lstrip('0')
    time = time.lower()
    return time

def current_temp():

    """arg: Uses the arduino temperature sensor to get data.
    return: The temperature."""

    global temperature
    humidity, temperature, timestamp = board.dht_read(DHTPIN)
    return temperature

def setup():

    """arg: Connects the arduino with the code you're running in visual studio code, 
    as well as the equipment used on the rich shield on top of the Arduino.
    return: Arduino connection and rich shield."""

    global board
    board = CustomPymata4(com_port = "COM6")
    board.set_pin_mode_digital_input_pullup(BUTTON2)
    board.set_pin_mode_digital_input_pullup(BUTTON1)
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05)
    board.set_pin_mode_tone(3)

def countdown(t):

    """arg: Countdown that you can set to a fixed time, formatted into minutes and seconds.
    return: a timer with mintues and seconds"""

    while t > 0:
        global timer
        mins, secs = divmod(t, 60)
        timer = '{:02d}.{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
        board.displayShow(timer)
        board.digital_write(RED_LED, 1)
        if t == 0:
            break

def oven1(t):
    global data
    global response
    global buttonState2
    with open('generations.csv', 'w', newline='') as gens:
        while True:
                mins, secs = divmod(t, 60)
                timer = '{:02d}.{:02d}'.format(mins, secs)
                print(timer, end="\r")
                time.sleep(1)
                t -= 1
                board.displayShow(timer)
                board.digital_write(RED_LED, 1)
                if t == 1:
                    return "pizza is ready"
                data = [timer, current_temp, current_time, "sensorID: 4942167"]
                dataCSV = [current_time()]
                writer = csv.writer(gens)
                writer.writerow(dataCSV)
                time.sleep(5)
                print("working")
                jsonData = {'countdown' : timer,
                'time' : current_time(),
                'temp' : current_temp()}
                response = requests.post("http://127.0.0.1:5000/orderUpdate", json = jsonData)
                buttonState2 = board.digital_read(BUTTON1)
                print("working")
                if BUTTON1 == 0:
                    board.digital_write(RED_LED, 0)
                    board.digital_write(GREEN_LED, 1)
                    board.play_tone(3, 1000, 1000)
                    return print ('shutdown oven')

setup()
if BUTTON2 == 0:
    oven1(900)