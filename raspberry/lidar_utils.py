import sys
import serial

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

