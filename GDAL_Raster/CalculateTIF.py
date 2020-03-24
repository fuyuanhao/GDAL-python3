# -*- coding: utf-8 -*-
import numpy as np
import gdal
import os
import matplotlib.pyplot as plt
from GDAL_Raster.OpenTIF import read_img,read_tif
from GDAL_Raster.WriteTIF import write_image,write_tif
import GDAL_Raster.ShowTIF as showTIF

#--------------------测试NDVI计算并输出栅格-------------------
#计算NDVI
#data原始影像
#outputname输出NDVI文件名
def NDVI_Calculation(imagepath):
    #引入OpenTIF中的图像读取方法读图像数据
    dataset = read_img(imagepath)
    #获取文件名【不包含后缀名】
    shorFilename = imagepath.split('.')[0]
    #将栅格数据转为数组并定义为数据类型为float
    data = dataset.ReadAsArray().astype(np.float)
    #由于数组是从0开始计数，因此波段名称为0，1，2，3；3为近红外波段；2为红波段
    ndvi = (data[3]-data[2])/(data[3]+data[2])
    #输出的NDVI文件名
    outputname= shorFilename+"_NDVI.tif"
    print('outputname:'+outputname)
    #调用栅格输出函数，输出NDVI，并指定为GTiff格式
    write_image(dataset,outputname,ndvi,"GTiff")
    print(outputname+'已成功生成！')
    NDVI_data = read_img(outputname)
    #窗口显示
    showTIF.ListShowTIFF(NDVI_data)
    #showTIF.ShowTIFFBoxplot(NDVI_data)

#波段重组4to3,234
def ComBandsTIFF(inputfile,outfilename):

    proj,geotrans,data,row1,column1 =read_tif(inputfile)
    data1=data[0]
    data2=data[1]
    data3=data[2]
    data4=data[3]

    bands_array = np.array((data2,data3, data4),dtype = data2.dtype)
    print(bands_array)
    write_tif(outfilename, proj, geotrans, bands_array)


#主函数
if __name__ == '__main__':
    #获取工程根目录的路径
    rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    #print('rootPath:'+rootPath)
    #数据文件路径
    dataPath = os.path.abspath(rootPath + r'\RasterData')
    #print('dataPath:'+dataPath)
    #切换目录
    os.chdir(dataPath)
    #测试影像数据
    imagepath ='S2_20190727San.tif'
    #调用NDVI计算方法
    NDVI_Calculation(imagepath)
    #filename = 'S2_20190727San_234.tif'
    #ComBandsTIFF(imagepath,filename)