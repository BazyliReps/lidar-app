from time import sleep
import RPi.GPIO as GPIO
import sys
import serial
import threading

ser = serial.Serial ('/dev/serial0',115200,timeout = 1)




def get_distance():
    if ser.is_open == False:
        ser.open()
    ser.write(bytes(b'B'))
    ser.write(bytes(b'W'))
    ser.write(bytes(2))
    ser.write(bytes(0))
    ser.write(bytes(0))
    ser.write(bytes(0))
    ser.write(bytes(1))
    ser.write(bytes(6))
        
    dist = 0
    ser.reset_input_buffer()
    running = True
    count = ser.in_waiting
    while(count < 8):
        count = ser.in_waiting
    recv = ser.read(9)
    ser.reset_input_buffer()
    if recv[0] == 'Y' and recv[1] == 'Y':
        low_dist = int(recv[2].encode('hex'), 16)
        high_dist = int(recv[3].encode('hex'), 16)
        dist = low_dist + high_dist * 256
        low_strength = int(recv[4].encode('hex'), 16)
        high_strength = int(recv[5].encode('hex'), 16)
        strength = low_strength + high_strength * 256
        ser.reset_input_buffer()
    if ser != None:
        ser.close()
    return [dist, strength]

def turn(mode, delay1):
    #GPIO.setmode(GPIO.BOARD)
    #GPIO.setwarnings(True)
    steps = 200    
    DIR = 20    #GPIO Pin DIR
    STEP = 21    #GPIO Pin STEP
    CW = 1
    CCW = 0
    steps *= mode
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.output(DIR, CW)
    

    MODE = (17, 27, 22)
    GPIO.setup(MODE, GPIO.OUT)
    
    RESOLUTION = {    1 : (0, 0, 0),
              2 : (1, 0, 0),
              4 : (0, 1, 0),
              8 : (1, 1, 0),
              16 : (0, 0, 1),
              32 : (1, 0, 1)}
    GPIO.output(MODE, RESOLUTION[mode])
    

    points = list()
    for x in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay1)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay1)
        [dist,strength] = get_distance()
        points.append((x,dist,strength))
    
    GPIO.output(DIR, CCW)
    
    for x in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay1)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay1)
    
    GPIO.cleanup()
    return points



