from time import sleep
from gpiozero import MCP3008
import RPi.GPIO as GPIO
import sys
import serial
import threading

ser = serial.Serial ('/dev/serial0',115200,timeout = 1)


def turn(mode, delay, del2, steps_to_lose):
    
    sensitivity = 0.9

    steps = 200    
    DIR = 20    #GPIO pin DIR
    STEP = 21   #GPIO pin STEP
    STATE = 16  #GPIO pin SLEEP
    SLEEP = 0
    WORK = 1
    CW = 1
    CCW = 0
    steps *= mode
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.setup(STATE, GPIO.OUT)
    GPIO.output(DIR, CW)
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
        print(x)
    
    sleep(1)
    GPIO.output(DIR, CCW)
    
    for x in range(steps - steps_to_lose):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    
    searching = True
    ORIENTATION = CCW

    sleep(1)
    lost_steps = 1
    while True:
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        sleep(del2)
        str = res.value
        if str > sensitivity:
            print("zgubiono %d moc %f" %(lost_steps, str))
            return
        lost_steps += 1    
        
    





    GPIO.output(STATE, SLEEP)
    GPIO.cleanup()
    return points

def main():
    mode = int(sys.argv[1])
    d1 = float(sys.argv[2])
    d2 = float(sys.argv[3])
    steps_to_lose = int(sys.argv[4])
    turn(mode, d1, d2, steps_to_lose)
    
if __name__ == "__main__":
    main()



