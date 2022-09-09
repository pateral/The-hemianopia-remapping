from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import cv2

left_image = cv2.imread("./mask_l.jpg")
right_image = cv2.imread("./mask_r.jpg")
# overlap = cv2.bitwise_or(left_image,right_image)
cv2.imshow("1",left_image)
cv2.imshow("2",right_image)
# cv2.imshow("overlap",overlap)
cv2.waitKey(0)
