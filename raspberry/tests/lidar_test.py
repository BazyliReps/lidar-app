from time import sleep
import RPi.GPIO as GPIO
import sys
import serial
import threading

ser = serial.Serial ('/dev/ttyAMA0',115200,timeout = 1)




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
    dist = 0
    strength = 0
    ser.reset_input_buffer()
    if recv[0] == 0x59 and recv[1] == 0x59:
        distance = recv[2] + recv[3] * 256
        strength = recv[4] + recv[5] * 256
        print(distance)
        ser.reset_input_buffer()
    if ser != None:
        ser.close()
    return [dist, strength]

def turn(mode, delay, del2):
  
  
    while True:
        print(get_distance())
    

def main():
    turn(2, 0.001, 0.01)
    
if __name__ == "__main__":
    main()





