from time import sleep
import RPi.GPIO as GPIO
import sys
import serial
import threading

ser = serial.Serial ('/dev/serial0',115200,timeout = 1)




def get_distance():
    if ser.is_open == False:
        ser.open()

    #ser.write(serial.to_bytes([0x42,0x57,0x02,0x00,0x00,0x00,0x00,0x1A]))
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
    if recv[0] == 'Y' and recv[1] == 'Y':
        low_dist = int(recv[2].encode('hex'), 16)
        high_dist = int(recv[3].encode('hex'), 16)
        dist = low_dist + high_dist * 256
        print(dist)
        low_strength = int(recv[4].encode('hex'), 16)
        high_strength = int(recv[5].encode('hex'), 16)
        strength = low_strength + high_strength * 256
        ser.reset_input_buffer()
    if ser != None:
        ser.close()
    return [dist, strength]

def turn(mode, delay, del2):
    #GPIO.setmode(GPIO.BOARD)
    #GPIO.setwarnings(True)

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
    

    points = list()
    for x in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        sleep(del2)
       # [dist,strength] = get_distance()
       # points.append((x,dist,strength))
    
    GPIO.output(DIR, CCW)
    
    for x in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    GPIO.output(STATE, SLEEP)
    GPIO.cleanup()
    return points


def main():
    mode = int(sys.argv[1])
    d1 = float(sys.argv[2])
    d2 = float(sys.argv[3])
    print("mode : %d d1: %f d2: %f" % (mode, d1, d2)) 
    turn(mode, d1, d2)
    
if __name__ == "__main__":
    main()





