# _*_ coding: cp936 _*_
# 导入geopandas
import geopandas,os
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point

#用来正常显示中文标签
#plt.rcParams['font.sans-serif']=['SimHei']
#plt.rcParams['figure.dpi'] = 200 #分辨率

#利用geopandas将点转shp数据并绘图
#要求EXCEL表中的经纬度字段名称分别为：LONGITUDE,LATITUDE；
#ExcelFile：文件名【包含路径】
def point2shp(ExcelFile):
    #geopandas自带数据，后面要加上编码，否则中文会变成乱码
    Exceldata = pd.read_excel(ExcelFile,encoding ="utf-8")
    #print(Exceldata)
    #经度信息
    x = Exceldata.LONGITUDE
    #print(x)
    #纬度信息
    y = Exceldata.LATITUDE
    #print(y)
    #坐标，几何信息
    xy = [Point(xy) for xy in zip(x,y)]
    #定义地理空间数据,将EXCEL信息和几何信息赋值
    pointDataFrame = geopandas.GeoDataFrame(Exceldata,geometry=xy)
    #设定投影坐标系为WGS84地理坐标系，编号为"EPSG:4326"
    pointDataFrame.crs="EPSG:4326"
    print(pointDataFrame.head())
    #获取文件名【不包含后缀名】
    shorFilename = ExcelFile.split('.')[0]
    #输出缓冲区后矢量文件名
    VectorFile= shorFilename+".shp"
    #输出Shp,设置编码格式，否则中文会有乱码
    pointDataFrame.to_file(VectorFile,'ESRI Shapefile',encoding ="utf-8")
    #空间数据制图
    pointDataFrame.plot(color='green')
    #显示结果
    plt.show()


#主函数

if __name__ == '__main__':
    #获取工程根目录的路径
    rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    #print('rootPath:'+rootPath)
    #数据文件路径
    dataPath = os.path.abspath(rootPath + r'\ShpData')
    #print('dataPath:'+dataPath)
    #切换目录
    os.chdir(dataPath)
    #EXCEL文件名
    ExcelFile ="fengjing.xlsx"

    #调用EXCEL点转矢量函数
    point2shp(ExcelFile)