from time import sleep
import RPi.GPIO as GPIO
import sys
import serial
from gpiozero import MCP3008
from find_laser_dot import find




def calibrate(start_x, camera, cv2, np):
    sensitivity = 0.4
    missed_steppes_scan = 0
    missed_steppes_return = 0


    DIR = 20     #GPIO DIR
    STEP = 21    #GPIO STEP
    CW = 0
    CCW = 1
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.output(DIR, CCW)

    
    sleep(0.1)
    res = MCP3008(0)

    MODE = (17, 27, 22)
    GPIO.setup(MODE, GPIO.OUT)
    
    RESOLUTION = {    1 : (0, 0, 0),
              2 : (1, 0, 0),
              4 : (0, 1, 0),
              8 : (1, 1, 0),
              16 : (0, 0, 1),
              32 : (1, 0, 1)}
    
    GPIO.output(MODE, RESOLUTION[2])
    
    new_x = find(camera, cv2, np)
    if abs(new_x - start_x) < 5:
        print("trafilem w cel, wychodze")
        return 
    
    print("docelowy x: %d, obecny x: %d" %(start_x, new_x))
    if new_x < start_x:
        GPIO.output(DIR, CW)
        print("laser na lewo")
    else:
        GPIO.output(DIR, CCW)
        print("laser na prawo")

    print("kalibruje po powrocie")
    sleep(0.1)
    for x in range(20):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(0.001)
        GPIO.output(STEP, GPIO.LOW)
        sleep(0.001)
        sleep(0.05)
        str = res.value
        if str > sensitivity:
            missed_steppes_return = x + 1
            break

    print("skonczylem!")
    return



