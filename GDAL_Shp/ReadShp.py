# -*- coding: cp936 -*-
import os

try:
    from osgeo import gdal
    from osgeo import ogr
except ImportError:
    import gdal
    import ogr

# 获取SHP字段信息
# oDefn为图层对象
def getFieldInfo(oDefn):
    #字段个数
    iFieldCount = oDefn.GetFieldCount()
    print('字段个数:'+ str(iFieldCount))
    #遍历所有字段
    for iAttr in range(iFieldCount):
        #字段对象
        oField = oDefn.GetFieldDefn(iAttr)
        #输出字段信息；python中较长的语句如果一行写不完可以用“\”来连接多行语句
        #Python格式化输出%s和%d 可参考博客https://www.cnblogs.com/linguansheng/p/10184102.html

        print("%s: %s(%d.%d)" % ( \
            #字段名称
            oField.GetNameRef(), \
            #字段类型
            oField.GetFieldTypeName(oField.GetType()), \
            #字段长度
            oField.GetWidth(), \
            #字段精度
            oField.GetPrecision()))


def ReadVectorFile(strVectorFile):
    # 为了支持中文路径，请添加下面这句代码
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # 为了使属性表字段支持中文，请添加下面这句，设置编码方式为GB2312
    #gdal.SetConfigOption("SHAPE_ENCODING", "GB2312")
    # 注册所有的驱动
    ogr.RegisterAll()
    # 打开数据
    ds = ogr.Open(strVectorFile, 0)
    #判断文件是否存在
    if ds == None:
        print("打开文件%s失败！" % strVectorFile)
        return
    #提示打开成功
    print("打开文件%s成功！" % strVectorFile)

    # 获取该数据源中的图层个数，一般shp数据图层只有一个，如果是mdb、dxf等图层就会有多个
    iLayerCount = ds.GetLayerCount()

    # 获取第一个图层
    oLayer = ds.GetLayerByIndex(0)
    if oLayer == None:
        print("获取第%d个图层失败！\n", 0)
        return

    # 对图层进行初始化，如果对图层进行了过滤操作，执行这句后，之前的过滤全部清空
    oLayer.ResetReading()

    # 通过属性表的SQL语句对图层中的要素进行筛选，这部分详细参考SQL查询章节内容
    #oLayer.SetAttributeFilter("\"NAME\"LIKE \"Hubei\"")

    # 通过指定的几何对象对图层中的要素进行筛选
    # oLayer.SetSpatialFilter()

    # 通过指定的四至范围对图层中的要素进行筛选
    # oLayer.SetSpatialFilterRect()

    # 获取图层中的属性表表头并输出
    print("属性表结构信息：")
    #图层对象
    oDefn = oLayer.GetLayerDefn()
    #字段个数
    iFieldCount = oDefn.GetFieldCount()
    print('字段个数: %d个' % iFieldCount)
    #遍历所有字段
    for iAttr in range(iFieldCount):
        #字段对象
        oField = oDefn.GetFieldDefn(iAttr)
        #输出字段信息；python中较长的语句如果一行写不完可以用“\”来连接多行语句
        #Python格式化输出%s和%d 可参考博客https://www.cnblogs.com/linguansheng/p/10184102.html

        print("%s: %s(%d.%d)" % ( \
            #字段名称
            oField.GetNameRef(), \
            #字段类型
            oField.GetFieldTypeName(oField.GetType()), \
            #字段长度
            oField.GetWidth(), \
            #字段精度
            oField.GetPrecision()))

    # 输出图层中的要素个数
    print("要素个数：%d个" % oLayer.GetFeatureCount(0))
    #定义新要素对象
    oFeature = oLayer.GetNextFeature()
    # 下面开始遍历图层中的要素
    while oFeature is not None:
        print("当前读取第 %d 个: \n属性值：" % (oFeature.GetFID()+1))
        # 获取要素中的属性表内容
        for iField in range(iFieldCount):
            #字段对象的属性信息
            oFieldDefn = oDefn.GetFieldDefn(iField)
            #构建行显示方式：字段名称+字段内容
            line = " %s (%s) = " % ( \
                #字段名称
                oFieldDefn.GetNameRef(), \
                #字段属性
                ogr.GetFieldTypeName(oFieldDefn.GetType()))

            #判断要素的字段集
            if oFeature.IsFieldSet(iField):
                #将要素属性转为字段串格式
                line = line + "%s" % (oFeature.GetFieldAsString(iField))
            else:
                line = line + "(null)"

            print('line:' + line)
            #print('line:' + line.encode('gbk','ignore').decode('cp936'))
            #print('line:' + line.encode('gbk','ignore').decode('cp936'))
            #print('line:'+line.encode('UTF-8', 'ignore').decode('UTF-8'))

        # 获取下一个要素
        oFeature = oLayer.GetNextFeature()
    print("数据集关闭！")

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
    strVectorFile ="wh_district.shp"
    #调用测试函数
    ReadVectorFile(strVectorFile)