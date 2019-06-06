from time import sleep
from stepper_utils import step, calibrate, set_stepper_mode, is_on_spot, change_direction, set_clockwise, set_counterclockwise
from lidar_utils import get_distance

delay2 = 0.03

def turn(mode, delay1):
    missed_steppes_scan = 0
    missed_steppes_return = 0
    set_stepper_mode(mode)
    direction = set_counterclockwise()

    steps = 200    
    steps *= mode

    sleep(0.1)
    print("skanuje w trybie 1/%d" %(mode))
    sleep(0.1)
    points = list()
    for x in range(steps):
        step(delay1,0)
        [dist,strength] = get_distance()
        points.append((x,dist,strength))
    
    if not is_on_spot():
        missed_steppes_scan = calibrate(delay1, delay2, mode)
        print("zgubiono %d krokow podczas skanu!" %(missed_steppes_scan))
    
    change_direction(direction)
    for x in range(steps):
        step(delay1, 0)
    
    sleep(0.5)   
    if not is_on_spot():
        missed_steppes_return = calibrate(delay1, delay2, mode)
        print("zgubiono %d krokow podczas powrotu!" %(missed_steppes_return))
    

    return points, missed_steppes_scan, missed_steppes_return   


def main():
    mode = 2
    d1 = 0.001
    turn(mode, d1)


if __name__ == "__main__":
    main()
