from time import sleep
import RPi.GPIO as GPIO
import sys
import serial
from gpiozero import MCP3008
from find_laser_dot import find

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
    ser.write(bytes(0))
    ser.write(bytes(26))
    dist = 0
    ser.reset_input_buffer()
    running = True
    count = ser.in_waiting
    while(count < 8):
        count = ser.in_waiting
    recv = ser.read(9)
    ser.reset_input_buffer()
    if recv[0] == 0x59 and recv[1] == 0x59:     
        distance = recv[2] + recv[3] * 256
        strength = recv[4] + recv[5] * 256
        ser.reset_input_buffer()
    if ser != None:
        ser.close()
    return [distance, strength]

def turn(mode, delay, camera, cv2, np, start_x):
    sensitivity = 0.9
    missed_steppes_scan = 0
    missed_steppes_return = 0


    steps = 200    
    STATE = 16   #GPIO SLEEP
    DIR = 20     #GPIO DIR
    STEP = 21    #GPIO STEP
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
    GPIO.output(DIR, CCW)
    GPIO.setup(STATE, GPIO.OUT)
    GPIO.output(STATE, WORK)

    

    res = MCP3008(0)

    MODE = (17, 27, 22)
    GPIO.setup(MODE, GPIO.OUT)
    
    RESOLUTION = {    1 : (0, 0, 0),
              2 : (1, 0, 0),
              4 : (0, 1, 0),
              8 : (1, 1, 0),
              16 : (0, 0, 1),
              32 : (1, 0, 1)}
    
    GPIO.output(MODE, RESOLUTION[mode])
    print("skanuje")
    points = list()
    for x in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        [dist,strength] = get_distance()
        points.append((x,dist,strength))
    
    str = res.value
    calibrate = True
    if str > sensitivity:
        calibrate = False
    print("kalibruje po skanie")
    GPIO.output(MODE, RESOLUTION[2])
    sleep(1)
    while calibrate:
        missed_steppes_scan += 1
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        sleep(0.05)
        str = res.value
        if str > sensitivity:
            print("[pomiar]: zgubiono %d krokow moc %f" %(missed_steppes_scan, str))
            break
        missed_steppes_scan += 1

    GPIO.output(MODE, RESOLUTION[mode])
    sleep(0.1)
    GPIO.output(DIR, CW)
    sleep(0.1)
    print("wracam")
    for x in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)

    str = res.value
    if str > sensitivity:
        return points, missed_steppes_scan, missed_steppes_return
    print("po powrocie moc: %f" %(str))
    new_x = find(camera, cv2, np)
    print("docelowy x: %d, obecny x: %d" %(start_x, new_x))
    if new_x < start_x:
        GPIO.output(DIR, CW)
        print("laser na lewo")
    else:
        GPIO.output(DIR, CCW)
        print("laser na prawo")

    sleep(2)
    print("kalibruje po powrocie")
    GPIO.output(MODE, RESOLUTION[2])
    sleep(0.1)
    for x in range(20):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        sleep(0.05)
        str = res.value
        if str > sensitivity:
            
            print("[powrot]: zgubiono %d krokow moc %f" %(x + 1, str))
            missed_steppes_return = x + 1
            break

    GPIO.output(STATE, SLEEP)
    GPIO.cleanup()
    return points, missed_steppes_scan, missed_steppes_return



