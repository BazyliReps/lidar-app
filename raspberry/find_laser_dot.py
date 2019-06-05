import io

def find(camera, cv2, np):
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg')
    data = np.fromstring(stream.getvalue(), dtype=np.uint8)

    img = cv2.imdecode(data, 1)
    
    blur= cv2.medianBlur(img, 7)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    
    
    lower_red = np.array([0,0,240])
    upper_red = np.array([150,150,255])
    
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,20,param1=20,param2=9,
                                   minRadius=4,maxRadius=15)
    
    
    index = 0
    if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                return x
