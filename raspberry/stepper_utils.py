from time import sleep
from gpiozero import MCP3008
import RPi.GPIO as GPIO
import sys

sensitivity = 0.8
DIR = 20    #GPIO pin DIR
STEP = 21   #GPIO pin STEP
CW = 1
CCW = 0
STATE = 16
MODE = (17, 27, 22)
RESOLUTION = {    1 : (0, 0, 0),
          2 : (1, 0, 0),
          4 : (0, 1, 0),
          8 : (1, 1, 0),
          16 : (0, 0, 1),
          32 : (1, 0, 1)}
res = MCP3008(0)

def turn_stepper_on():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.output(DIR, CCW)
    GPIO.setup(MODE, GPIO.OUT)
    GPIO.setup(STATE, GPIO.OUT)
    GPIO.output(STATE,1)
    GPIO.output(MODE, RESOLUTION[2])


def set_clockwise():
    GPIO.output(DIR, CW)
    return CW


def set_counterclockwise():
    GPIO.output(DIR, CCW)
    return CCW

def set_stepper_mode(mode):
    GPIO.output(MODE, RESOLUTION[mode])


def calibrate(d1,d2,mode):
    set_stepper_mode(2)
    scale = 2
    direction = CCW
    while True:
        for s in range(scale):
            step(d1, d2)
            str = res.value
            if is_on_spot():
                sleep(0.01)
                set_stepper_mode(mode)
                return s 
        
        direction = change_direction(direction)
        
        for s in range(scale):
            step(d1, d2)
        
        scale *= 2

        for s in range(scale):
            step(d1, d2)
            str = res.value
            if is_on_spot():
                sleep(0.01)
                set_stepper_mode(mode)
                return s 
        
        direction = change_direction(direction)
        
        for s in range(scale):
            step(d1, d2)


def is_on_spot():
    return res.value > sensitivity


def change_direction(direction):
    direction = abs(direction - 1)
    GPIO.output(DIR, direction)
    sleep(0.1)
    return direction

def step(d1, d2):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(d1)                       
    GPIO.output(STEP, GPIO.LOW)
    sleep(d1)
    sleep(d2)

