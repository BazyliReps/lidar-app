from time import sleep
import RPi.GPIO as GPIO
from stepper_utils import step, calibrate, set_stepper_mode, is_on_spot, change_direction
from lidar_utils import get_distance

delay2 = 0.001

def turn(mode, delay1):
    missed_steppes_scan = 0
    missed_steppes_return = 0

    set_stepper_mode(mode)

    steps = 200    
    steps *= mode

    sleep(0.1)
    print("skanuje")
    sleep(0.1)
    points = list()
    for x in range(steps):
        step(delay1,0)
        [dist,strength] = get_distance()
        points.append((x,dist,strength))
    
    if not is_on_spot():
        missed_steppes_scan = calibrate(delay1, delay2)
    
    change_direction()
    for x in range(steps):
        step(delay1, 0)
    
    if not is_on_spot():
        missed_steppes_return = calibrate(delay1, delay2)
    

    return points, missed_steppes_scan, missed_steppes_return   


def main():
    mode = 2
    d1 = 0.001
    turn(mode, d1)


if __name__ == "__main__":
    main()
