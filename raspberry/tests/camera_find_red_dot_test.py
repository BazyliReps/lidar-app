import numpy as np
import cv2
from picamera import PiCamera
import io
camera = PiCamera()
camera.resolution = (1024, 768)
#camera.capture('laser.jpg')



#img = cv2.imread('laser.jpg')
stream = io.BytesIO()
camera.capture(stream, format='jpeg')
data = np.fromstring(stream.getvalue(), dtype=np.uint8)

img = cv2.imdecode(data, 1)

blur= cv2.medianBlur(img, 5)
hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)


lower_red = np.array([0,0,240])
upper_red = np.array([150,150,255])

mask = cv2.inRange(hsv, lower_red, upper_red)

circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,20,param1=20,param2=8,
                               minRadius=3,maxRadius=30)


print(circles)
index = 0
if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            print("x: %f" %(x))
            index = index + 1
        print("No. of circles detected = %s" %(format(index)))
