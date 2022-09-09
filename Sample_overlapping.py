import numpy as np #1
import cv2 #2

canvas = np.zeros((300, 300, 3), dtype="uint8") #3
(centerX, centerY) = (canvas.shape[1] // 2 - 5, canvas.shape[0] // 2 ) #23
white = (255, 255, 255) #24

cv2.circle(canvas, (centerX, centerY), 50, white,-1)  #26
cv2.circle(canvas, (centerX + 10, centerY ), 50, white,-1)
cv2.imshow("Canvas", canvas) #27
cv2.imwrite("sample_tolerate.png",canvas)
cv2.waitKey(0)