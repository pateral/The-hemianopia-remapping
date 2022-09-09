from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
import cv2




right = 1
if right == 1:
    a = np.load(r"C:\Users\59105\Desktop\Graduation\demo\FW__Supervisor_Allocation\MSc_project_2238976l\VisualRemapper-main\Program\dot_positions_r.npy")
else:
    a = np.load(
        r"C:\Users\59105\Desktop\Graduation\demo\FW__Supervisor_Allocation\MSc_project_2238976l\VisualRemapper-main\Program\dot_positions_l.npy")
points_storage = a.tolist()
print(points_storage)
#CALCULATE THE SIZE
list_length = len(points_storage)
min_x = points_storage[0][0]
min_y = points_storage[0][1]
max_x = points_storage[0][0]
max_y = points_storage[0][1]
for i in range(0, 20, 1):
    if min_x >= points_storage[i][0]:
        min_x = points_storage[i][0]

    if max_x <= points_storage[i][0]:
        max_x = points_storage[i][0]

    if min_y >= points_storage[i][1]:
        min_y = points_storage[i][1]

    if max_y <= points_storage[i][1]:
        max_y = points_storage[i][1]
range_x = max_x - min_x
range_y = max_y - min_y
print([range_x, range_y])

for i in range(0,20,1):
     points_storage[i][0] -= min_x
     points_storage[i][1] -= min_y




if right == 1:
    img = cv2.imread(
        r"C:\Users\59105\Desktop\Graduation\demo\FW__Supervisor_Allocation\MSc_project_2238976l\VisualRemapper-main\Stereo_DepthMap-master\image\teddy\cones\im6.png")
else:
    img = cv2.imread(
        r"C:\Users\59105\Desktop\Graduation\demo\FW__Supervisor_Allocation\MSc_project_2238976l\VisualRemapper-main\Stereo_DepthMap-master\image\teddy\cones\im2.png")
#tention: cv2 is  bgr format，we should use the method :cv2.cvtColor() to transfer to rgb
img_use = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#注意img为numpy.ndarray图片数据，需用如下方法转化为PIL所需数据类型
img = Image.fromarray(img_use)
target_size = (range_x, range_y)
#将图片缩放到目标大小，不改变原数据，需将得到结果赋值给新变量
new_image = img.resize(target_size)
new_h, new_w = new_image.size
print('new_img_size:', new_h, new_w)

fig = plt.figure(figsize=(24, 24))
#原图片
#add_subplot()前面两个参数表示将fig划分为几乘几的网格，每个网格中可以放一张图片，最后一个数字表示放在第几个网格中，亦可写为：211
a = fig.add_subplot(3, 1, 1)
plt.imshow(img)
a.set_title('Before')
#缩放后的图片
a = fig.add_subplot(3,1,2)
plt.imshow(new_image)
a.set_title('After')




new_image = np.asarray(new_image)
new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
if right == 1:
    cv2.imwrite("new_image_right.jpg", new_image)
    new_image = cv2.imread("new_image_right.jpg")
else:
    cv2.imwrite("new_image_left.jpg", new_image)
    new_image = cv2.imread("new_image_left.jpg")
##注释区
pts = np.array(points_storage)
pts = np.array([pts])
mask = np.zeros(new_image.shape[:2], np.uint8)

# print(np.asarray(new_image))
# print(mask)
# # 在mask上将多边形区域填充为白色
mask = cv2.polylines(mask, pts, 1, 0)    # 描绘边缘
mask = cv2.fillPoly(mask, pts, 255)    # 填充
# #
# cv2.imwrite("new_image.jpg", new_image)
# new_img = cv2.imread(r"./new_image.jpg")


# mask = cv2.bitwise_and(new_img, new_img, mask=mask)

#deal = cv2.bitwise_and(new_image,)
dst = cv2.bitwise_and(new_image, new_image, mask=mask)
# # # 添加白色背景
bg = np.ones_like(new_image, np.uint8) * 255
cv2.bitwise_not(bg, bg, mask=mask)  # bg的多边形区域为0，背景区域为255
dst_white = bg + dst
#
a = fig.add_subplot(3, 1, 3)
plt.imshow(dst)
a.set_title('dst')

if right == 1:
    cv2.imwrite("mask_r.jpg", mask)
    cv2.imwrite("dst_r.jpg", dst)
    cv2.imwrite("dst_white_r.jpg", dst_white)
else:
    cv2.imwrite("mask_l.jpg", mask)
    cv2.imwrite("dst_l.jpg", dst)
    cv2.imwrite("dst_white_l.jpg", dst_white)

plt.show()