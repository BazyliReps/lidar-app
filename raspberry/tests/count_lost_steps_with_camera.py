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

def turn(mode, delay, del2, offset):
    
    sensitivity = 0.9
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
    GPIO.output(DIR, CCW)
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
    
    camera = PiCamera()
    camera.resolution = (1024, 768)

    start_x = find(camera, cv2, np)
    print("poczatkowa pozycja lasera: %d" %(start_x))

    points = list()
    for x in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        sleep(del2)
    
    
    str = res.value
    calibrate = True
    if str > sensitivity:
        calibrate = False

    lost_steps = 0
    
    while calibrate:
        lost_steps += 1
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        sleep(0.05)
        str = res.value
        if str > sensitivity:
            print("[pomiar]: zgubiono %d krokow moc %f" %(lost_steps, str))
            break
        lost_steps += 1
    

    GPIO.output(DIR, CW)
    for x in range(steps + offset) :
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)

    str = res.value
    if str > sensitivity:
        print("trafilem w sedno!")
        return
       
    new_x = find(camera, cv2, np)
    print("koncowa pozycja lasera: %d" %(new_x))

    if new_x < start_x:
        GPIO.output(DIR, CW)
        print("laser przesuniety w lewo!")
    else:
        GPIO.output(DIR, CCW)
        print("laser przesuniety w prawo!")
    print("aktualna moc: %f" %(str))    
    
    for x in range(10):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        sleep(0.05)
        str = res.value
        if str > 0.8:
            print("[powrot]: zgubiono %d krokow moc %f" %(x+1, str))
            sleep(0.01)
            break
                                                

    GPIO.output(STATE, SLEEP)
    GPIO.cleanup()
    return

def main():
    mode = int(sys.argv[1])
    d1 = float(sys.argv[2])
    d2 = float(sys.argv[3])
    offset = int(sys.argv[4])
    turn(mode, d1, d2, offset)
    
if __name__ == "__main__":
    main()



