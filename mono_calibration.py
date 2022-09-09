#-*- coding:utf-8 -*-
import os.path
import numpy as np
import cv2
import glob

#-------------------------------
# 设置棋盘格大小  objp和Size 参数
# 单目以./image/left/下目录图片为例子
#-------------------------------
Checkerboard = (9,6)  #棋盘格内角点数
square_size = (10,10)   #棋盘格大小，单位mm
scale = square_size[0]
# 设置迭代终止条件
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 设置 object points, 形式为 (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((Checkerboard[0]*Checkerboard[1],3), np.float32) #我用的是12*8的棋盘格，可根据自己棋盘格自行修改相关参数
# objp[:,:2] = np.mgrid[0:Checkerboard[0],0:Checkerboard[1]].T.reshape(-1,2)
objp[:, :2] = np.mgrid[0:(Checkerboard[0]-1)*scale:complex(0,Checkerboard[0]),
              0:(Checkerboard[1]-1)*scale:complex(0,Checkerboard[1])].T.reshape(-1, 2)

# 用arrays存储所有图片的object points 和 image points
objpoints = [] # 3d point in real world space  #存放世界坐标系下角点位置
imgpoints = [] # 2d points in image plane.    #存放左图像坐标系下角点位置
grays = []

#用glob匹配文件夹/home/song/pic_1/right/下所有文件名含有“.jpg"的图片
images = glob.glob(r"./image/left/*.jpg")
print("一共"+str(len(images))+"张图片")
for fname in images:
    img = cv2.imread(fname)
    # 转灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 查找棋盘格角点
    ret, corners = cv2.findChessboardCorners(gray, Checkerboard, None)
    # 如果找到了就添加 object points, image points
    if ret == True:
        objpoints.append(objp)
        # 亚像素操作
        corners2=cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # 对角点连接画线加以展示
        cv2.drawChessboardCorners(img, Checkerboard, corners2, ret)
        cv2.imshow('img', img)

        print("请敲击任意键，检测下一帧角点...")
        cv2.waitKey()

    else:
        print("检测角点失败...,请检查图片路径或者棋盘格大小")
cv2.destroyAllWindows()

# 标定
#  mtx内参3*3，dist畸变，rvecs旋转向量，tvecs平移向量，
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print("相机内参：\n",mtx, "\n相机畸变：\n",dist)

#对所有图片进行去畸变，有两种方法实现分别为： undistort()和remap()
images = glob.glob(r"./img/left/*.jpg")
if not os.path.exists("undistort"):
    os.mkdir("undistort")
for fname in images:
    prefix=fname.split('/')[-1]
    img = cv2.imread(fname)
    h,  w = img.shape[:2]

    #-----------------------------
    # getOptimalNewCameraMatrix
    # 去畸变后的图像四周会出现黑色区域，如果畸变较大，如鱼眼镜头，四周黑色区域将会更大。
    # opencv中给我们提供了一个函数getOptimalNewCameraMatrix()，用于去除畸变矫正后图像四周黑色的区域。
    #
    # 该函数根据给定参数alpha计算最优的新相机内参矩阵。alpha = 0，则去除所有黑色区域，alpha = 1，则保留所有原始图像像素，
    # 其他值则得到介于两者之间的效果。
    #
    # 通过该函数，我们得到新的相机内参矩阵，然后利用initUndistortRectifyMap()即可获得用于remap()的映射矩阵。
    # ------------------------------

    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

    # # 使用 cv.undistort()进行畸变校正
    # dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    # # 对图片有效区域进行剪裁
    # # x, y, w, h = roi
    # # dst = dst[y:y+h, x:x+w]
    # cv2.imwrite('undistort/'+prefix, dst)

    #  使用 remap() 函数进行校正
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
    # 对图片有效区域进行剪裁
    x, y, w, h = roi
    dst = dst[y:y + h, x:x + w]
    cv2.imwrite('./undistort/'+prefix, dst)

#重投影误差计算
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error

print("total error: ", mean_error/len(objpoints))

# 保存结果
result = "cameraMatrix：\n"+str(mtx)+"\ndistCoeff：\n"+str(dist)+"\ntotal error:\n"+str(mean_error/len(objpoints))
save_path = "result/mono_calib.txt"
with open(save_path,'w') as f:
    f.write(result)
f.close()
print("save result successfully...")