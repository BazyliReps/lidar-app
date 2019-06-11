from time import sleep
from gpiozero import MCP3008
import RPi.GPIO as GPIO
import sys
import serial
import threading

ser = serial.Serial ('/dev/serial0',115200,timeout = 1)

DIR = 20    #GPIO pin DIR
STEP = 21   #GPIO pin STEP
STATE = 16  #GPIO pin SLEEP
SLEEP = 0
WORK = 1
CW = 1
CCW = 0

def turn(mode, d1, d2):
    
    sensitivity = 0.8

    steps = 200    
    steps *= mode
    GPIO.setwarnings(True)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.setup(STATE, GPIO.OUT)
    GPIO.output(DIR, CW)
    GPIO.output(STATE, WORK)

    sleep(2)   

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
        step(d1, d2)
    

    GPIO.output(DIR, CCW)
    
    for x in range(steps - 7):
        step(d1, 0)
    sleep(2)
    searching = True
    ORIENTATION = CCW

    scale = 2
    print(range(scale))   
    while searching:
        print("1sza wychylka %d krokow" %(scale))
        for s in range(scale):
            step(d1, d2)
            str = res.value
            if str > sensitivity:
                sleep(0.01)
                print("zgubiono %d krokow" %(s))
                return s 
        GPIO.output(DIR, CW)    
        print("powrot1 %d krokow" %(scale))
        for s in range(scale):
            step(d1, d2)
        
        scale *= 2

        print("2ga wychylka %d krokow" %(scale))
        for s in range(scale):
            step(d1, d2)
            str = res.value
            if str > sensitivity:
                sleep(0.01)
                print("zgubiono %d krokow" %(s))
                return s 
        
        GPIO.output(DIR, CCW)
        print("powrot2 %d krokow" %(scale))
        for s in range(scale):
            step(d1, d2)

    #GPIO.output(STATE, SLEEP)
    sleep(5)
    GPIO.cleanup()
    return points

def step(d1, d2):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(d1)                       
    GPIO.output(STEP, GPIO.LOW)
    sleep(d1)
    sleep(d2)


def change_dir(DIR, ORIENTATION):
    if ORIENTATION == 0:
        ORIENTATION = 1
    else:
        ORIENTATION = 0
    GPIO.output(DIR, ORIENTATION)    

def main():
    mode = 2#int(sys.argv[1])
    d1 = 0.001#float(sys.argv[2])
    d2 = 0.01#float(sys.argv[3])
    print("mode : %d d1: %f d2: %f" % (mode, d1, d2)) 
    turn(mode, d1, d2)
    
if __name__ == "__main__":
    main()



