# _*_ coding: cp936 _*_
# ����geopandas
import geopandas,os
from fiona.crs import from_epsg
from geopandas import GeoSeries
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# ����������ʾ���ı�ǩ
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False # ��ʾ����

# ����ʸ������
# �뾶radius,��λ��m
def ShpBuffer(strVectorFile,radius):
    # geopandas�����ݣ��������ģ���������ı��뷽ʽ�����������ַ�������վ���ӵȣ�����utf-8��ʽ
    vector = geopandas.read_file(strVectorFile)
    print('------------��������-----------------')
    print(vector.crs)

    print('------------ͶӰת��-----------------')
    # EPSG:32649:WGS 84 / Area of use: Between 108��E and 114��E, northern hemisphere between equator and 84��N, onshore and offshore.
    vector_utm = vector.to_crs("epsg:32649")
    # ��ӡ�������ͶӰ��Ϣ
    print(vector_utm.crs)
    # ��ӡ�������������
    print(vector_utm.head())

    print('----------------------buffer-------------------------------')
    # ��ȡ����ʸ�����ݵļ�����Ϣ
    g = GeoSeries(vector_utm['geometry'])
    # �������������뾶Ϊ�������������radius
    buffer=g.buffer(radius)
    # ��ͼ�ĵ�ͼ���ã���ɫ��򣬰�ɫ�ڲ�
    base = vector_utm.plot(color='white',edgecolor='darkgreen')
    # ԭʼ�����ʸ���ļ���ͼ����ɫ
    buffer.plot(ax=base, color='lime')
    # ��������ͼ��ͳһ��ͼ���ԱȻ���ǰ����
    plt.show()

    # �������������û����ļ�����Ϣ
    vector_buffer = vector_utm.set_geometry(buffer)
    print(vector_buffer.head())
    # �����������ʸ�����ݶ���ͶӰ=����ʸ���ļ�ͶӰ
    vector_buffer.crs = "EPSG:32649"
    # print(vector_buffer.crs)
    # ��ȡ�ļ�������������׺����
    shorFilename = strVectorFile.split('.')[0]
    # �����������ʸ���ļ���
    bufferVectorFile= shorFilename+"_buffer_"+str(radius)+"m.shp"
    # �������ļ����ָ���ļ���
    #vector_buffer.to_file(bufferVectorFile,'ESRI Shapefile',encoding ="utf-8")
    return bufferVectorFile

def ShpDissolve(strVectorFile):
    vector = geopandas.read_file(strVectorFile)
    #print(vector.head())
    vector = vector[['��', 'geometry']]
    onevector = vector.dissolve(by='��')
    onevector.plot(color='white', edgecolor='gold')
    plt.show()
    print('----------------------dissolve-------------------------------')
    print(onevector.head())
    return onevector

def ShpIntersection(strBuffer_a, strBuffer_b,dissolve_a,dissolve_b):
    buffer_a = geopandas.read_file(strBuffer_a)
    buffer_b = geopandas.read_file(strBuffer_b)
    res_intersection = geopandas.overlay(buffer_a, dissolve_b, how='intersection')
    print('-----------------------�ཻ���----------------------------')
    print(res_intersection)
    # �ȶ��建�������ݣ���������
    ax = dissolve_a.plot(alpha=0.7, facecolor='lime')
    bx = dissolve_b.plot(alpha=0.7, facecolor='lime')
    # �ٶ����ཻ���ͼ�㣬�����ϲ�
    res_intersection.plot(ax=bx, alpha=0.5, facecolor='tomato')  # ,marker='o', markersize=5
    plt.title('intersection')
    plt.show()

#������
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

