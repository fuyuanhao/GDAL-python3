# _*_ coding: cp936 _*_
# ����geopandas
import geopandas,os
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point

#����������ʾ���ı�ǩ
#plt.rcParams['font.sans-serif']=['SimHei']
#plt.rcParams['figure.dpi'] = 200 #�ֱ���

#����geopandas����תshp���ݲ���ͼ
#Ҫ��EXCEL���еľ�γ���ֶ����Ʒֱ�Ϊ��LONGITUDE,LATITUDE��
#ExcelFile���ļ���������·����
def point2shp(ExcelFile):
    #geopandas�Դ����ݣ�����Ҫ���ϱ��룬�������Ļ�������
    Exceldata = pd.read_excel(ExcelFile,encoding ="utf-8")
    #print(Exceldata)
    #������Ϣ
    x = Exceldata.LONGITUDE
    #print(x)
    #γ����Ϣ
    y = Exceldata.LATITUDE
    #print(y)
    #���꣬������Ϣ
    xy = [Point(xy) for xy in zip(x,y)]
    #�������ռ�����,��EXCEL��Ϣ�ͼ�����Ϣ��ֵ
    pointDataFrame = geopandas.GeoDataFrame(Exceldata,geometry=xy)
    #�趨ͶӰ����ϵΪWGS84��������ϵ�����Ϊ"EPSG:4326"
    pointDataFrame.crs="EPSG:4326"
    print(pointDataFrame.head())
    #��ȡ�ļ�������������׺����
    shorFilename = ExcelFile.split('.')[0]
    #�����������ʸ���ļ���
    VectorFile= shorFilename+".shp"
    #���Shp,���ñ����ʽ���������Ļ�������
    pointDataFrame.to_file(VectorFile,'ESRI Shapefile',encoding ="utf-8")
    #�ռ�������ͼ
    pointDataFrame.plot(color='green')
    #��ʾ���
    plt.show()


#������

if __name__ == '__main__':
    #��ȡ���̸�Ŀ¼��·��
    rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    #print('rootPath:'+rootPath)
    #�����ļ�·��
    dataPath = os.path.abspath(rootPath + r'\ShpData')
    #print('dataPath:'+dataPath)
    #�л�Ŀ¼
    os.chdir(dataPath)
    #EXCEL�ļ���
    ExcelFile ="fengjing.xlsx"

    #����EXCEL��תʸ������
    point2shp(ExcelFile)