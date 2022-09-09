
from PIL import Image
import math
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt









theta = 15
left_image = Image.open(r"C:\Users\59105\Desktop\Graduation\demo\FW__Supervisor_Allocation\MSc_project_2238976l\VisualRemapper-main\TheSimpleBase\dst_l.jpg")
right_image = Image.open(r"C:\Users\59105\Desktop\Graduation\demo\FW__Supervisor_Allocation\MSc_project_2238976l\VisualRemapper-main\TheSimpleBase\dst_r.jpg")

left_image.rotate(-theta).save("left_rotation.png")#旋转45度

right_image.rotate(theta).save("right_rotation.png")




# 错切
alpha = 5/180*math.pi
shearM = np.array([
    [1, math.tan(alpha), -225*math.tan(alpha)],
    [0, 1,   0]
], dtype=np.float32)

img = cv.imread('left_rotation.png')
img_shear = cv.warpAffine(img, shearM, dsize=(450, 434))

cv.imwrite("consequence.png",img_shear)



cv.WaitKey(0)