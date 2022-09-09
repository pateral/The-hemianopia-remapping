import numpy as np #1
import cv2 #2
import math

canvas = np.zeros((500, 500, 3), dtype="uint8") #3
(centerX, centerY) = (canvas.shape[1] // 2, canvas.shape[0] // 2) #23
white = (255, 255, 255) #24
Mode = 3
rate = 0.2
if Mode == 1:
    for centerX in range(50, 500, 150):   #25
        for centerY in range(50, 500, 150):
            cv2.circle(canvas, (centerX, centerY), 30, white,-1)  #26

if Mode == 2:
    unit = 15
    cv2.circle(canvas, (centerX,centerY), 10, white, -1)
    for length in range (-10, 11 , 1):
        for theta in range(0,180,30):
            if length!= 0:
                distance = math.pow(1+rate,abs(length))*unit*(length/abs(length))

                x = centerX + distance*math.cos(theta/180*math.pi)
                y = centerY + distance*math.sin(theta/180*math.pi)
                cv2.circle(canvas, (int(x),int(y)), 6, white, -1)

if Mode == 3:
    unit = 50
    x = 490
    for i in range(0,10,1):
        use = unit*pow(1+rate,i)
        x = int(x - use)
        for j in range(-4,5,1):
            y = int(centerY + j*unit)
            cv2.circle(canvas, (x, y), 6, white, -1)
cv2.imshow("Canvas", canvas) #27
cv2.imwrite("evaluation_image_0.2_l.png",canvas)


cv2.waitKey(0)  #28
