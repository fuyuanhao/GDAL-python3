#-*- coding: cp936 -*-
import os
try:
    from osgeo import gdal
    from osgeo import ogr
    from osgeo import osr
except ImportError:
    import gdal
    import ogr

def WriteVectorFile(strVectorFile):
    # 为了支持中文路径，请添加下面这句代码
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8","NO")
    # 为了使属性表字段支持中文，请添加下面这句
    gdal.SetConfigOption("SHAPE_ENCODING","GB2312")

    # 注册所有的驱动
    ogr.RegisterAll()

    # 创建数据，这里以创建ESRI的shp文件为例
    strDriverName = "ESRI Shapefile"
    oDriver =ogr.GetDriverByName(strDriverName)
    if oDriver == None:
        print("%s 驱动不可用！\n", strDriverName)
        return

    # 创建数据源
    oDS =oDriver.CreateDataSource(strVectorFile)
    if oDS == None:
        print("创建文件%s失败！" % strVectorFile)
        return

    #定义投影
    targetSR = osr.SpatialReference()
    targetSR.ImportFromEPSG(4326) #Geo WGS84
    # 创建图层，创建一个多边形图层，这里没有指定空间参考，如果需要的话，需要在这里进行指定
    papszLCO = []
    oLayer =oDS.CreateLayer("TestPolygon", targetSR, ogr.wkbPolygon, papszLCO)
    if oLayer == None:
        print("图层创建失败！\n")
        return

    # ----------------------下面创建属性表----------------------------
    # 先创建一个叫FieldID的整型属性
    oFieldID =ogr.FieldDefn("FieldID", ogr.OFTInteger)
    oLayer.CreateField(oFieldID, 1)

    # 再创建一个叫FieldName的字符型属性，字符长度为100
    oFieldName =ogr.FieldDefn("FieldName", ogr.OFTString)
    oFieldName.SetWidth(100)
    oLayer.CreateField(oFieldName, 1)

    #--------------------------创建要素--------------------------------
    oDefn = oLayer.GetLayerDefn()

    # 创建三角形要素
    oFeatureTriangle = ogr.Feature(oDefn)
    #设置字段属性值
    oFeatureTriangle.SetField(0, 0)
    oFeatureTriangle.SetField(1, "三角形")
    #给空间要素赋三角形顶点坐标值----点连成面
    geomTriangle =ogr.CreateGeometryFromWkt("POLYGON ((0 0,20 0,10 15,0 0))")
    #给要素设置几何属性
    oFeatureTriangle.SetGeometry(geomTriangle)
    #生成要素
    oLayer.CreateFeature(oFeatureTriangle)

    # 创建矩形要素
    oFeatureRectangle = ogr.Feature(oDefn)
    oFeatureRectangle.SetField(0, 1)
    oFeatureRectangle.SetField(1, "矩形")
    geomRectangle =ogr.CreateGeometryFromWkt("POLYGON ((30 0,60 0,60 30,30 30,30 0))")
    oFeatureRectangle.SetGeometry(geomRectangle)
    oLayer.CreateFeature(oFeatureRectangle)

    # 创建五角星要素
    oFeatureStar = ogr.Feature(oDefn)
    oFeatureStar.SetField(0, 2)
    oFeatureStar.SetField(1, "五角星")
    geomStar = ogr.CreateGeometryFromWkt("POLYGON ((175 92,155 152,95 154,143 191,126 251,175 217,223 250,207 192,255 154,196 151))")
    oFeatureStar.SetGeometry(geomStar)
    oLayer.CreateFeature(oFeatureStar)

    # 创建点要素
    # oFeaturePoint = ogr.Feature(oDefn)
    # oFeaturePoint.SetField(0, 2)
    # oFeaturePoint.SetField(1, "点")
    # #geomPoint =ogr.CreateGeometryFromWkt("Point(10,20)")
    # geomPoint = ogr.Geometry(ogr.wkbPoint)
    # geomPoint.AddPoint(10,20)
    # oFeaturePoint.SetGeometry(geomPoint)
    # oLayer.CreateFeature(oFeaturePoint)

    oDS.Destroy()
    print("数据集创建完成！\n")

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
    strVectorFile ="TestPolygon.shp"
    #测试
    WriteVectorFile(strVectorFile)