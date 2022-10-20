from datetime import datetime
import time 
import requests
from fhict_cb_01.CustomPymata4 import CustomPymata4
from datetime import datetime
import time

DHTPIN = 12
RED_LED = 4
GREEN_LED = 5
BUTTON2 = 9
BUTTON1 = 8
BUZZER = 3
BUTTON_PRESSED = 0

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

def manual_shut_off():

    """arg: This function makes it so that if there is a manual shutdown of the arduino (button click) a unique message will appear.
    Return: the ovenResponse is Off"""

    time.sleep(0.1)
    global ovenResponse
    global timer
    ovenResponse = "Off"
    board.digital_write(RED_LED, 0)
    board.digital_write(GREEN_LED, 1)
    board.play_tone(3, 1000, 1000)
    print('shutdown oven')
    timer = '00.00'
    return

def timer_end():

    """arg: if the timer ends this means the pizza is ready, so it needs a unique message.
    return: the ovenResponse is pizza is ready"""

    global timer
    global ovenResponse
    board.digital_write(RED_LED, 0)
    board.digital_write(GREEN_LED, 1)
    board.play_tone(3, 1000, 1000)
    timer = '00.00'
    ovenResponse = "Pizza is ready"
    print ("pizza is ready")

def send_data_to_app():

    """arg: everytime the while loop for the oven breaks it will send the last needed data to the flask server to keep the html up to date as well.
    retrun: the current arduino data, current time and ovenResponse."""

    global response
    jsonData = {'ovenResponse' : ovenResponse,
    'countdown' : timer,
    'time' : current_time(),
    'temp' : current_temp()}
    response = requests.post("http://127.0.0.1:5000/orderUpdate", json = jsonData)

def oven1(t):

    """arg: oven1 function creates puts all needed function together so that the arduino data, timer for the oven will be added.
    return: current time, the timer for the pizza, temperature and the button to manually stop """

    global ovenResponse
    global timer
    global response
    with open('generations.csv', 'w', newline='') as gens:
        while True:
            mins, secs = divmod(t, 60)
            timer = '{:02d}.{:02d}'.format(mins, secs)
            print(timer, end="\r")
            t -= 1
            board.displayShow(timer)
            board.digital_write(GREEN_LED, 0)
            board.digital_write(RED_LED, 1)
            if t == 0:
                timer_end()
                send_data_to_app()
                break
            time.sleep(0.7)
            send_data_to_app()
            buttonState2 = board.digital_read(BUTTON2)
            if (buttonState2[0] == BUTTON_PRESSED):
                manual_shut_off()
                send_data_to_app()
                break
setup()
time.sleep(0.1)
while True:
    time.sleep(0.1)
    buttonState1 = board.digital_read(BUTTON1)
    if (buttonState1[0] == BUTTON_PRESSED):
        ovenResponse = "On"
        print("oven is on")
        oven1(10)