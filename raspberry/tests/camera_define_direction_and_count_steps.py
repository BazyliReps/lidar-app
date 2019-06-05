from time import sleep
from gpiozero import MCP3008
import RPi.GPIO as GPIO
import sys
import serial
import threading
import cv2
import numpy as np
from bare_find_dot import find
from picamera import PiCamera



def turn(mode, delay, del2):
    
    sensivity = 0.9
    steps = 200    
    DIR = 20    #GPIO pin DIR
    STEP = 21   #GPIO pin STEP
    STATE = 16  #GPIO pin SLEEP
    SLEEP = 0
    WORK = 1
    CW = 0
    CCW = 1
    steps *= mode
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.setup(STATE, GPIO.OUT)
    
    GPIO.output(STATE, SLEEP)
    
    camera = PiCamera()
    camera.resolution = (1024, 768)

    x = find(camera, cv2, np)
    print("x poczatkowe: %d. przesun laser!" %(x))
    for i in range(5):
        print(i)
        sleep(1)
    

    new_x = find(camera, cv2, np)
    print(new_x)
    
    if new_x < x:
        GPIO.output(DIR, CW)
        print("laser przesuniety w lewo!")
    else:
        GPIO.output(DIR, CCW)
        print("laser przesuniety w prawo!")
    sleep(1)

    GPIO.output(STATE, WORK)

    

    MODE = (17, 27, 22)
    GPIO.setup(MODE, GPIO.OUT)
    
    RESOLUTION = {    1 : (0, 0, 0),
              2 : (1, 0, 0),
              4 : (0, 1, 0),
              8 : (1, 1, 0),
              16 : (0, 0, 1),
              32 : (1, 0, 1)}
    GPIO.output(MODE, RESOLUTION[mode])
    res = MCP3008(0)
    

    points = list()
    for x in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        sleep(del2)
        str = res.value
        if str > sensivity:
            sleep(0.01)
            return
    

def main():
    mode = 2#int(sys.argv[1])
    d1 = 0.001#float(sys.argv[2])
    d2 = 0.05#float(sys.argv[3])
    turn(mode, d1, d2)
    
if __name__ == "__main__":
    main()



