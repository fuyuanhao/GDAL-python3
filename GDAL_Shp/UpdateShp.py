import sys,os
from osgeo import gdal
from osgeo import ogr

#更新shp文件，新增字段并更新属性值
def UpdateShp(pathname):
    # 为了支持中文路径，请添加下面这句代码
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # 为了使属性表字段支持中文，请添加下面这句
    gdal.SetConfigOption("SHAPE_ENCODING", "GB2312")
    # 注册所有的驱动
    ogr.RegisterAll()
    # 数据格式的驱动
    driver = ogr.GetDriverByName('ESRI Shapefile')
    #打开文件
    ds = driver.Open(pathname, update=1)
    if ds is None:
        print('Could not open %s' % pathname)
        sys.exit(1)
    # 获取第0个图层
    oLayer = ds.GetLayerByIndex(0)
    # 投影
    spatialRef = oLayer.GetSpatialRef()
    # 输出图层中的要素个数
    print ('要素个数=%d' % (oLayer.GetFeatureCount(0)))
    print ('属性表结构信息')

    #图层对象
    defn = oLayer.GetLayerDefn()
    #字段索引，指定字段
    xfieldindex = defn.GetFieldIndex('FieldName')
    #获取指定索引的字段对象
    xfield = defn.GetFieldDefn(xfieldindex)
    #新建字段x
    fieldDefn = ogr.FieldDefn('x', xfield.GetType())
    #字段宽度
    fieldDefn.SetWidth(100)
    #创建字段
    oLayer.CreateField(fieldDefn,1)
    yfieldindex = defn.GetFieldIndex('FieldID')
    #获取指定索引的字段对象
    yfield = defn.GetFieldDefn(yfieldindex)
    #创建字段y
    fieldDefn = ogr.FieldDefn('y', yfield.GetType())
    fieldDefn.SetWidth(32)
    fieldDefn.SetPrecision(6)
    oLayer.CreateField(fieldDefn,1)

    feature = oLayer.GetNextFeature()
    # 下面开始遍历图层中的要素
    while feature is not None:
        # 获取要素中的属性表内容
        FieldName = feature.GetFieldAsString('FieldName')
        print('FieldName:'+FieldName)
        FieldID = feature.GetFieldAsDouble('FieldID')
        print('FieldID:'+str(FieldID))
        #把字段FieldName对应的属性值赋值给新建字段newx1
        feature.SetField('x', FieldName)
        #把字段FieldID对应的属性值赋值给新建字段newy1
        feature.SetField('y', FieldID)
        #设定要素值，刷新
        oLayer.SetFeature(feature)
        #下一个要素
        feature = oLayer.GetNextFeature()
    #feature.Destroy()
    ds.Destroy()
    print('数据更新完成')

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
    UpdateShp(strVectorFile)
