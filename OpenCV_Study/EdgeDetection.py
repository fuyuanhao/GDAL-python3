#coding:utf-8
import cv2,os
import numpy as np
from matplotlib import pyplot as plt

#用来正常显示中文标签
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['font.sans-serif']=['Times New Roman']
plt.rcParams['axes.unicode_minus'] = False# 显示负号
plt.rcParams['figure.dpi'] = 100 #分辨率

#图像轮廓提取
def CV_findContours(img):
    image = cv2.imread(img)
    image = cv2.resize(image, None, fx=0.7, fy=0.7)    #为了完整显示，缩小一倍
    print(image)

    fig = plt.gcf()                                  #分通道显示图片
    fig.set_size_inches(10, 15)

    plt.subplot(221)
    plt.imshow(np.flip(image, axis=2))
    plt.axis('off')
    plt.title('Image')

    #ShaHu.png
    BGR = np.array([60,65,65])
    #CrayfishRice.jpg,水体
    #BGR = np.array([122,141,140])
    #水稻
    #BGR = np.array([48,93,65])
    #油菜
    #BGR = np.array([20,180,190])
    upper = BGR + 10
    lower = BGR - 10
    mask = cv2.inRange(image,lower,upper)
    #cv2.imshow("Mask",mask)

    plt.subplot(222)
    plt.imshow(mask, cmap='gray')
    plt.axis('off')
    plt.title('Mask')

    #使用cv2.findContours()函数对mask图片提取轮廓，并调用cv2.drawContour()把轮廓叠加在原始图像
    contours,hicrarchy = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    print("number of contours:%d" %(len(contours)))
    alllakesImage = image.copy()
    cv2.drawContours(alllakesImage,contours,-1,(0,0,255),2)
    #cv2.imshow("Image of All Lake",alllakesImage)

    plt.subplot(223)
    plt.imshow(alllakesImage)
    plt.axis('off')
    plt.title('All Contours')

    #在获取的轮廓结果图中我们可以看到，存在众多的细小板块，统计结果显示number of contours，
    # #其中contours.sort(key=len,reverse=True)可以对细小斑块的面积进行排序
    theLargestLake = image.copy()
    contours.sort(key=len,reverse=True)
    #显示第一和第二大的轮廓线
    cv2.drawContours(theLargestLake,[contours[0]],-1,(0,0,255),2)
    #cv2.imshow("Image of the Largest Lake",theLargestLake)

    plt.subplot(224)
    plt.imshow(theLargestLake)
    plt.axis('off')
    plt.title('Big Contours')

    plt.show()
    #cv2.waitKey(0)#代表由手动确定下一步操作，否则会出现显示图像一闪而过的情况，或是出现图像无响应的情况
    #cv2.destroyAllWindows()#销毁内存

def CannyEdge(imgFile):
    #-------------------------------------
    img = cv2.imread(imgFile, 0)
    #img = cv2.resize(img, None, fx=0.3, fy=0.3)    #为了完整显示，缩小一倍
    img = cv2.GaussianBlur(img,(3,3),0) # 用高斯平滑处理原图像降噪。若效果不好可调节高斯核大小
    cv2.imshow('GaussianBlur', img)

    canny = cv2.Canny(img, 0, 45)     # 调用Canny函数，指定最大和最小阈值，其中apertureSize默认为3。

    cv2.imshow('Canny', canny)
    cv2.waitKey(0)
    cv2.destroyAllWindows()#销毁内存


def SobelEdge(imgFile):
    # Sobel边缘检测算子
    img = cv2.imread(imgFile, 0)
    #img = cv2.resize(img, None, fx=0.3, fy=0.3)    #为了完整显示，缩小一倍
    x = cv2.Sobel(img, cv2.CV_16S, 1, 0)
    y = cv2.Sobel(img, cv2.CV_16S, 0, 1)
    # cv2.convertScaleAbs(src[, dst[, alpha[, beta]]])
    # 可选参数alpha是伸缩系数，beta是加到结果上的一个值，结果返回uint类型的图像
    Scale_absX = cv2.convertScaleAbs(x)  # convert 转换  scale 缩放
    Scale_absY = cv2.convertScaleAbs(y)
    result = cv2.addWeighted(Scale_absX, 0.5, Scale_absY, 0.5, 0)
    cv2.imshow('img', img)
    cv2.imshow('Scale_absX', Scale_absX)
    cv2.imshow('Scale_absY', Scale_absY)
    cv2.imshow('result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def LaplacianEdge(imgFile):
    img = cv2.imread(imgFile, 0)
    #img = cv2.resize(img, None, fx=0.3, fy=0.3)    #为了完整显示，缩小一倍
    laplacian = cv2.Laplacian(img, cv2.CV_16S, ksize=3)
    dst = cv2.convertScaleAbs(laplacian)
    cv2.imshow('laplacian', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__=='__main__':
    #获取工程根目录的路径
    rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    #print('rootPath:'+rootPath)
    #数据文件路径
    dataPath = os.path.abspath(rootPath + r'\Image')
    #print('dataPath:'+dataPath)
    #切换目录
    os.chdir(dataPath)
    #SHP文件路径
    imgFile ="cat.jpg"
    #cvshowbasicimg(imgFile)
    #CV_findContours(imgFile)
    #CannyEdge(imgFile)
    #SobelEdge(imgFile)
    LaplacianEdge(imgFile)