# -*- coding: utf-8 -*-
import os
try:
    from osgeo import gdal
    from osgeo import ogr
except ImportError:
    import gdal
    import ogr

def ReadVectorFile(strVectorFile):
    # 为了支持中文路径，请添加下面这句代码
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # 为了使属性表字段支持中文，请添加下面这句
    gdal.SetConfigOption("SHAPE_ENCODING", "GB2312")

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

#主函数
if __name__ == '__main__':
    #获取工程根目录的路径
    rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    print('rootPath:'+rootPath)
    #数据文件路径
    dataPath = os.path.abspath(rootPath + r'\ShpData')
    print('dataPath:'+dataPath)
    #切换目录
    os.chdir(dataPath)
    strVectorFile ="TestPolygon.shp"
    #调用测试函数
    ReadVectorFile(strVectorFile)
