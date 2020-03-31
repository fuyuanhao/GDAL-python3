# _*_ coding: cp936 _*_
# 导入geopandas
import geopandas,os
from fiona.crs import from_epsg
from geopandas import GeoSeries
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# 用来正常显示中文标签
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False # 显示负号

# 输入矢量数据
# 半径radius,单位：m
def ShpBuffer(strVectorFile,radius):
    # geopandas打开数据，如有中文，则加上中文编码方式，如有特殊字符，如网站链接等，则用utf-8方式
    vector = geopandas.read_file(strVectorFile)
    print('------------输入数据-----------------')
    print(vector.crs)

    print('------------投影转换-----------------')
    # EPSG:32649:WGS 84 / Area of use: Between 108°E and 114°E, northern hemisphere between equator and 84°N, onshore and offshore.
    vector_utm = vector.to_crs("epsg:32649")
    # 打印输出数据投影信息
    print(vector_utm.crs)
    # 打印输出数据属性列
    print(vector_utm.head())

    print('----------------------buffer-------------------------------')
    # 获取输入矢量数据的几何信息
    g = GeoSeries(vector_utm['geometry'])
    # 缓冲区分析，半径为函数的输入参数radius
    buffer=g.buffer(radius)
    # 绘图的底图设置，黑色外框，白色内部
    base = vector_utm.plot(color='white',edgecolor='darkgreen')
    # 原始输入的矢量文件制图，绿色
    buffer.plot(ax=base, color='lime')
    # 上述两个图层统一制图，对比缓冲前后结果
    plt.show()

    # 缓冲区数据设置缓冲后的几何信息
    vector_buffer = vector_utm.set_geometry(buffer)
    print(vector_buffer.head())
    # 给缓冲区后的矢量数据定义投影=输入矢量文件投影
    vector_buffer.crs = "EPSG:32649"
    # print(vector_buffer.crs)
    # 获取文件名【不包含后缀名】
    shorFilename = strVectorFile.split('.')[0]
    # 输出缓冲区后矢量文件名
    bufferVectorFile= shorFilename+"_buffer_"+str(radius)+"m.shp"
    # 缓冲区文件输出指定文件夹
    #vector_buffer.to_file(bufferVectorFile,'ESRI Shapefile',encoding ="utf-8")
    return bufferVectorFile

def ShpDissolve(strVectorFile):
    vector = geopandas.read_file(strVectorFile)
    #print(vector.head())
    vector = vector[['市', 'geometry']]
    onevector = vector.dissolve(by='市')
    onevector.plot(color='white', edgecolor='gold')
    plt.show()
    print('----------------------dissolve-------------------------------')
    print(onevector.head())
    return onevector

def ShpIntersection(strBuffer_a, strBuffer_b,dissolve_a,dissolve_b):
    buffer_a = geopandas.read_file(strBuffer_a)
    buffer_b = geopandas.read_file(strBuffer_b)
    res_intersection = geopandas.overlay(buffer_a, dissolve_b, how='intersection')
    print('-----------------------相交结果----------------------------')
    print(res_intersection)
    # 先定义缓冲区数据，放在下面
    ax = dissolve_a.plot(alpha=0.7, facecolor='lime')
    bx = dissolve_b.plot(alpha=0.7, facecolor='lime')
    # 再定义相交结果图层，放在上层
    res_intersection.plot(ax=bx, alpha=0.5, facecolor='tomato')  # ,marker='o', markersize=5
    plt.title('intersection')
    plt.show()

#主函数
if __name__ == '__main__':
    rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    dataPath = os.path.abspath(rootPath + r'\ShpData')
    os.chdir(dataPath)
    strVectorFile_a ="fengjing.shp"
    #buffer_a = ShpBuffer(strVectorFile_a,500)
    strBuffer_a = 'fengjing_buffer_500m.shp'
    dissolve_a = ShpDissolve(strBuffer_a)
    strVectorFile_b = "canyin.shp"
    #buffer_b = ShpBuffer(strVectorFile_b, 500)
    strBuffer_b = 'canyin_buffer_500m.shp'
    dissolve_b = ShpDissolve(strBuffer_b)
    ShpIntersection(strBuffer_a, strBuffer_b, dissolve_a, dissolve_b)

