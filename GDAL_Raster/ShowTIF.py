# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from osgeo import gdal
import os,cv2
import numpy as np
import pandas as pd
from GDAL_Raster.OpenTIF import read_img

# 用来正常显示中文标签
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False# 显示负号
plt.rcParams['figure.dpi'] = 200 #分辨率
# 默认的像素：[6.0,4.0]，分辨率为100，图片尺寸为 600&400
# 指定dpi=200，图片尺寸为 1200*800
# 指定dpi=300，图片尺寸为 1800*1200
# 设置figsize可以在不改变分辨率情况下改变比例

# 显示简单数组
def showShortTIFF():
    a=np.arange(18).reshape(6,3)
    print(a)

    b=a[[0,1,2]]
    print(b)

    #定义图片框
    plt.figure()
    # 将画板分为1行两列，本幅图位于第一个位置
    plt.subplot(1,2,1)
    plt.title("彩色图片")
    #图片显示原始图像
    plt.imshow(a)
    plt.colorbar()
    # 将画板分为1行两列，本幅图位于第3个位置
    plt.subplot(1,2,2)
    plt.title("灰度图")
    # 加载灰度图，可以添加 cmap 参数解决
    plt.imshow(a, cmap='Greys_r')
    plt.colorbar()

    plt.show()

# 显示自然图像
def showShortImage():
    #打开指定图片
    a = plt.imread('xinghuaduotian.jpg')
    print(a.shape)

    plt.title("彩色图片")
    # 图片显示原始图像
    plt.imshow(a)
    # 定义图片框
    plt.figure()

    b=a[[0,1,2]]
    print('----------b----------')
    print(b.shape)
    c=b[:,[0,1,2]]
    print('----------c----------')
    print(c.shape)

    #将画板分为1行两列，本幅图位于第一个位置
    plt.subplot(1,2,1)
    plt.title("彩色图片")
    #图片显示原始图像
    plt.imshow(a)
    #plt.colorbar(shrink=0.75)
    # 将画板分为1行两列，本幅图位于第3个位置
    plt.subplot(1,2,2)
    plt.title("灰度图")
    im_r = a[:, :, 0]  # 单通道
    print('------------------单通道------------------------')
    print(im_r.shape)
    # 加载灰度图，可以添加 cmap 参数解决
    plt.imshow(im_r, cmap='Greys_r')
    #plt.colorbar(shrink=0.75)

    plt.show()

# 显示遥感影像某一波段灰度图
def showGreyTIFF(band):
    #将图片转为数组
    image = band.ReadAsArray()
    # 加载灰度图，可以添加 cmap 参数解决
    plt.imshow(image, cmap='Greys_r')
    plt.colorbar()
    plt.axis('off') # 不显示坐标轴
    #窗口中展示灰度图
    plt.show()

# 并排显示单波段信息
def ListShowTIFF(band):
    #将指定图片转为数组
    image = band.ReadAsArray()
    #定义图片框
    plt.figure()
    # 将画板分为两行两列，本幅图位于第一个位置
    plt.subplot(2,2,1)
    plt.title("彩色图片")
    #图片显示原始图像
    plt.imshow(image)
    plt.colorbar()
    plt.axis('off')
    # 将画板分为两行两列，本幅图位于第2个位置
    plt.subplot(2,2,2)
    plt.title("灰度图")
    # 加载灰度图，可以添加 cmap 参数解决
    plt.imshow(image, cmap='Greys_r')
    plt.colorbar()
    plt.axis('off')
    # 将画板分为两行两列，本幅图位于第3个位置
    plt.subplot(2,2,3)
    plt.title("直方图")
    plt.hist(image, facecolor='g',edgecolor='b')
    #plt.legend()
    #窗口中展示图片
    plt.show()

#  直方图统计
def ShowTIFFHist(band):
    #将指定图片转为数组
    image = band.ReadAsArray()
    plt.title("Histogram")
    plt.hist(image, facecolor='g',
             edgecolor='b',alpha=0.7)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    #plt.legend()
    #窗口中展示图片
    plt.show()

#直方图统计
def ShowTIFFBoxplot(band):
    #将指定图片转为数组
    image = band.ReadAsArray()
    df = pd.DataFrame(image)
    print('-------------describe-----------------')
    print(df.describe())

    df.plot.box(title="Box Plot")
    plt.grid(linestyle="--", alpha=0.8)
    plt.show()

# 显示遥感影像的所有单波段灰度图像
def showMultiBandTIFFGray(RasterData):
    #打开指定图片
    #image = RasterData.ReadAsArray()
    #定义图片框
    plt.figure()
    #获取波段数量
    num_bands= RasterData.ReadAsArray().shape[0]
    print('波段数为：'+str(num_bands))
    for index in range(num_bands):
        print(index+1)
        #获取各波段数据，索引是从0开始，0-3，而波段是从1开始，1-4，因此需要给index+1，否则GetRasterBand(0)会出错
        band = RasterData.GetRasterBand(index+1)
        #转数组
        band_data=band.ReadAsArray()

        # 将画板分为2行多列，各波段从左到右依次排列
        plt.subplot(2,num_bands,index+1)
        #图片标题
        plt.title("band"+str(index+1))
        #图片显示原始图像
        plt.imshow(band_data, cmap='Greys_r')

        plt.subplot(2,num_bands,index+1+num_bands)

        #计算平均值
        mean_band_data =np.mean(band_data)
        #标准差
        std_range = np.std(band_data)*2
        #图片显示拉伸后的图像
        plt.imshow(band_data, cmap='Greys_r',vmin=mean_band_data-std_range,vmax=mean_band_data+std_range)
        #plt.axis('off') # 不显示坐标轴
    #plt.colorbar(shrink=0.5)
    #窗口中展示图片
    plt.show()

# 显示彩色遥感影像
def showColorTIFF(RasterData,bandRindex=1,bandGindex=2,bandBindex=3):
    image_data = RasterData.ReadAsArray()
    band1 = RasterData.GetRasterBand(1).ReadAsArray()
    band2 = RasterData.GetRasterBand(2).ReadAsArray()
    band3 = RasterData.GetRasterBand(3).ReadAsArray()
    band4 = RasterData.GetRasterBand(4).ReadAsArray()
    #判断栅格数据的数据类型
    if 'int8' in image_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in image_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    bandR = band1 if bandRindex == 1 else band2 if bandRindex == 2 else band3 if bandRindex == 3 else band4
    bandG = band1 if bandGindex == 1 else band2 if bandGindex == 2 else band3 if bandGindex == 3 else band4
    bandB = band1 if bandBindex == 1 else band2 if bandBindex == 2 else band3 if bandBindex == 3 else band4
    # if(bandRindex == 1):
    #     bandR = band1
    # elif(bandRindex == 2):
    #     bandR = band2
    # elif(bandRindex == 3):
    #     bandR = band3
    # elif(bandRindex == 4):
    #     bandR = band4

    # matplotlib使用RGB格式，opencv使用的是BGR格式
    bands = np.array([bandR, bandG, bandB]).transpose((1, 2, 0))
    plt.imshow((bands * 255).astype(np.uint8))
    plt.colorbar()
    plt.axis('off')
    plt.show()

def normalizationOfBand(band):
    max = np.max(band)
    min = np.min(band)
    print(max,min)
    newband = (band - min) / (max - min)
    return newband

def QshowColorTIFF(strRasterData,bandRindex=4,bandGindex=3,bandBindex=2):
    RasterData = read_img(strRasterData)
    band1 = RasterData.GetRasterBand(1).ReadAsArray()
    band2 = RasterData.GetRasterBand(2).ReadAsArray()
    band3 = RasterData.GetRasterBand(3).ReadAsArray()
    band4 = RasterData.GetRasterBand(4).ReadAsArray()

    bandR = band1 if bandRindex == 1 else band2 if bandRindex == 2 else band3 if bandRindex == 3 else band4
    bandG = band1 if bandGindex == 1 else band2 if bandGindex == 2 else band3 if bandGindex == 3 else band4
    bandB = band1 if bandBindex == 1 else band2 if bandBindex == 2 else band3 if bandBindex == 3 else band4

    bandR = normalizationOfBand(bandR)
    bandG = normalizationOfBand(bandG)
    bandB = normalizationOfBand(bandB)
    # opencv使用的是BGR格式
    bands = np.array([bandB, bandG, bandR]).transpose((1, 2, 0))
    bands = (bands*255).astype(np.uint8)
    print(bands.shape)
    print(bands.size)
    print(bands.dtype)

    shortFilename = strRasterData.split('.')[0]  # 获取文件名【不包含后缀名】
    print(shortFilename)
    out_jpg = shortFilename + "_temp.jpg"  # 临时文件
    print('out_jpg:' + out_jpg)
    cv2.imwrite(out_jpg, bands)
    cv2.destroyAllWindows()  # 销毁内存
    return out_jpg


# 主函数
if __name__ == '__main__':
    #获取工程根目录的路径
    rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    #数据文件路径
    dataPath = os.path.abspath(rootPath + r'\RasterData')
    #切换目录
    os.chdir(dataPath)
    #测试影像数据
    imagepath ='S2_20190727San.tif'

    # 显示数组
    #showShortTIFF()
    # 显示自然图像
    #showShortImage()

    #引入OpenTIF中的图像读取方法读图像数据
    #dataset = read_img(imagepath)

    # 显示遥感影像某一波段灰度图
    #band1 = dataset.GetRasterBand(1)
    #showGreyTIFF(band1)
    #ListShowTIFF(band1)
    #ShowTIFFHist(band1)
    #ShowTIFFBoxplot(band1)

    # 显示遥感影像的所有单波段灰度图像
    #showMultiBandTIFFGray(dataset)

    # 显示彩色遥感影像
    QshowColorTIFF(imagepath,1,2,3)



