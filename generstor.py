from datetime import datetime
import time 
import requests
from fhict_cb_01.CustomPymata4 import CustomPymata4
from datetime import datetime
import time
import csv
import time, sys
from pynput.keyboard import Key, Controller #To make this import work, open command promt and put in "pip install pynput".

DHTPIN = 12
RED_LED = 4
GREEN_LED = 5
BUTTON1PIN = 8
BUZZER = 3
keyboard = Controller() #Function to make keys simulated in the code.

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
    board.set_pin_mode_digital_input_pullup(BUTTON1PIN)
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05)
    board.set_pin_mode_tone(3)

def countdown(t):

    """arg: Countdown that you can set to a fixed time, formatted into minutes and seconds.
    return: a timer with mintues and seconds"""

    while t:
        global pizzaStatus
        mins, secs = divmod(t, 60)
        timer = '{:02d}.{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
        board.displayShow(timer)
        board.digital_write(RED_LED, 1)
        if timer == 0:
            pizzaStatus = "The pizza is ready"
        else:
            pizzaStatus = "The pizza is not ready yet"

def button_press():

    """arg: button press on the rich shield converted to the keypresses ctrl + c
    return: button 1 on the rich shield is now ctrl + c"""

    level, time_stamp = board.digital_read(BUTTON1PIN)
    if level == 1:
        keyboard.press(Key.ctrl)
        keyboard.press('c')
        time.sleep(0.1)
        keyboard.release('c')
        keyboard.release(Key.ctrl)

setup()
with open('generations.csv', 'w', newline='') as gens:
    while True:
        button_press()
        data = [countdown, current_temp, current_time, "sensorID: 4942167"]
        dataCSV = [current_time()]
        writer = csv.writer(gens)
        writer.writerow(dataCSV)
        time.sleep(5)
        jsonData = {'countdown' : countdown(900),
        'time' : current_time(),
        'temp' : current_temp(),
        'pizza' : pizzaStatus}
        response = requests.post("http://127.0.0.1:5000/admin", json = jsonData)
        try:
            countdown(900)
        except KeyboardInterrupt: # crtl+C
            board.digital_write(RED_LED, 0)
            board.digital_write(GREEN_LED, 1)
            board.play_tone(3, 1000, 1000)
            print ('shutdown')
            board.shutdown()
            sys.exit(0)