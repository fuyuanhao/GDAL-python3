# coding:utf-8
import cv2,os
import numpy as np
from matplotlib import pyplot as plt

# 用来正常显示中文标签
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['font.sans-serif']=['Times New Roman']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 100

# 图片基本信息获取及不同效果显示
def cvshowbasicimg(imgFile):
    img = cv2.imread(imgFile,cv2.IMREAD_COLOR)
    #第二个参数是通道数和位深的参数，
    #IMREAD_UNCHANGED = -1#不进行转化，比如保存为了16位的图片，读取出来仍然为16位。
    #IMREAD_GRAYSCALE = 0#进行转化为灰度图，比如保存为了16位的图片，读取出来为8位，类型为CV_8UC1。
    #IMREAD_COLOR = 1#进行转化为RGB三通道图像，图像深度转为8位
    #IMREAD_ANYDEPTH = 2#保持图像深度不变，进行转化为灰度图。
    #IMREAD_ANYCOLOR = 4#若图像通道数小于等于3，则保持原通道数不变；若通道数大于3则只取取前三个通道。图像深度转为8位
    print(img.shape)#输出：高像素，宽像素，通道数
    print(img.size)#总通道数=高* 宽* 通道数
    print(img.dtype)#3个通道每个通道占的位数（8位，一个字节）
    print(cv2.mean(img))
    cv2.imshow("source",img)
    b,g,r=cv2.split(img)
    cv2.imshow("B",b)
    cv2.imshow("G",g)
    cv2.imshow("R",r)
    #得到灰度图片
    imgviewx2=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #二值化图像，黑白图像，只有0和1,0为0,1为255
    ret,imgviewx2=cv2.threshold(imgviewx2,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    title = 'Binary Image'#图片标题
    gbk_title=title.encode("gbk").decode(errors="ignore")#中文解码
    cv2.imshow(gbk_title,imgviewx2)#图片显示
    cv2.waitKey(0)#代表由手动确定下一步操作，否则会出现显示图像一闪而过的情况，或是出现图像无响应的情况
    cv2.destroyAllWindows()#销毁内存

# 灰度图直方图
def getGrayHist(img):

    img_bgr = cv2.imread(img, cv2.IMREAD_COLOR) #OpenCV读取颜色顺序：BRG

    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    fig = plt.gcf()
    fig.set_size_inches(8, 7.5)
    # 将画板分为1行2列，本幅图位于第1个位置
    plt.subplot(1,2,1)
    plt.imshow(img_gray, cmap='gray')
    plt.axis('off')
    plt.title('Gray')
    plt.colorbar(shrink=0.5)

    img_gray_hist = cv2.calcHist([img_gray], [0], None, [256], [0, 256])

    # 将画板分为1行2列，本幅图位于第2个位置
    plt.subplot(1,2,2)
    plt.plot(img_gray_hist)
    plt.title('Grayscale Histogram')
    plt.xlabel('Bins')
    plt.ylabel('# of Pixels')
    #plt.colorbar()

    plt.show()

# 获取RGB三个通道的直方图并绘制到一张图里
def getRGBHist(img):
    img_bgr = cv2.imread(img, cv2.IMREAD_COLOR) #OpenCV读取颜色顺序：BRG
    img_b = img_bgr[..., 0]
    img_g = img_bgr[..., 1]
    img_r = img_bgr[..., 2]
    fig = plt.gcf()                                  #分通道显示图片
    fig.set_size_inches(10, 15)

    plt.subplot(321)
    plt.imshow(np.flip(img_bgr, axis=2))             #展平图像数组并显示
    plt.axis('off')
    plt.title('Image')

    plt.subplot(322)
    plt.imshow(img_r, cmap='gray')
    plt.axis('off')
    plt.title('R')

    plt.subplot(323)
    plt.imshow(img_g, cmap='gray')
    plt.axis('off')
    plt.title('G')

    plt.subplot(324)
    plt.imshow(img_b, cmap='gray')
    plt.axis('off')
    plt.title('B')

    # 按R、G、B三个通道分别计算颜色直方图
    b_hist = cv2.calcHist([img_bgr], [0], None, [256], [0, 256])
    g_hist = cv2.calcHist([img_bgr], [1], None, [256], [0, 256])
    r_hist = cv2.calcHist([img_bgr], [2], None, [256], [0, 256])

    plt.subplot(313)
    # 显示3个通道的颜色直方图
    plt.plot(b_hist, label='B', color='blue')
    plt.plot(g_hist, label='G', color='green')
    plt.plot(r_hist, label='R', color='red')
    plt.legend(loc='best')
    plt.xlim([0, 256])
    plt.show()

# 获取RGB三个通道的直方图并绘制到一张图里
def getRGBHistOnebyOne(img):
    img_bgr = cv2.imread(img, cv2.IMREAD_COLOR) #OpenCV读取颜色顺序：BRG
    img_b = img_bgr[..., 0]
    img_g = img_bgr[..., 1]
    img_r = img_bgr[..., 2]

    # 按R、G、B三个通道分别计算颜色直方图
    b_hist = cv2.calcHist([img_bgr], [0], None, [256], [0, 256])
    g_hist = cv2.calcHist([img_bgr], [1], None, [256], [0, 256])
    r_hist = cv2.calcHist([img_bgr], [2], None, [256], [0, 256])

    fig = plt.gcf()                                  #分通道显示图片
    fig.set_size_inches(10, 15)

    plt.subplot(241)
    plt.imshow(np.flip(img_bgr, axis=2))             #展平图像数组并显示
    plt.axis('off')
    plt.title('Image')

    plt.subplot(242)
    plt.imshow(img_r, cmap='gray')
    plt.axis('off')
    plt.title('R')

    plt.subplot(243)
    plt.imshow(img_g, cmap='gray')
    plt.axis('off')
    plt.title('G')

    plt.subplot(244)
    plt.imshow(img_b, cmap='gray')
    plt.axis('off')
    plt.title('B')

    plt.subplot(245)
    # 显示3个通道的颜色直方图
    plt.plot(b_hist, label='B', color='blue')
    plt.plot(g_hist, label='G', color='green')
    plt.plot(r_hist, label='R', color='red')
    plt.legend(loc='best')
    plt.xlim([0, 256])

    plt.subplot(246)
    # 显示单个通道的颜色直方图
    plt.plot(r_hist, label='R', color='red')
    plt.legend(loc='best')
    plt.xlim([0, 256])

    plt.subplot(247)
    # 显示1个通道的颜色直方图
    plt.plot(g_hist, label='G', color='green')
    plt.legend(loc='best')
    plt.xlim([0, 256])

    plt.subplot(248)
    # 显示1个通道的颜色直方图
    plt.plot(b_hist, label='B', color='blue')
    plt.legend(loc='best')
    plt.xlim([0, 256])

    plt.show()

if __name__=='__main__':
    # 获取工程根目录的路径
    rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # 数据文件路径
    dataPath = os.path.abspath(rootPath + r'\Image')
    # 切换目录
    os.chdir(dataPath)
    imgFile ="cat.jpg"
    #cvshowbasicimg(imgFile)
    getGrayHist(imgFile)
    #getRGBHist(imgFile)
    #getRGBHistOnebyOne(imgFile)