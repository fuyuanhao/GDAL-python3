from osgeo import gdal
import os

#读图像文件函数
#输入参数：文件名
#返回参数im_data
def read_img(filename):
    #打开文件
    dataset=gdal.Open(filename)
    #栅格矩阵的列数
    im_width = dataset.RasterXSize
    print('-------栅格矩阵的列数---------')
    print(im_width)
    #栅格矩阵的行数
    im_height = dataset.RasterYSize
    print('-------栅格矩阵的行数---------')
    print(im_height)
    #地图投影信息
    im_proj = dataset.GetProjection()
    print('-------地图投影信息---------')
    print(im_proj)
    #将数据写成数组，对应栅格矩阵
    im_data = dataset.ReadAsArray(0,0,im_width,im_height)
    print('-------影像属性---波段数，行数，列数------')
    print(im_data.shape)
    print('-------栅格矩阵信息---------')
    print(im_data)
    print(im_data.dtype)
    #清除数据集缓存
    del im_data
    #返回获取的参数
    return dataset

def readF_img(filename):
    dataset=gdal.Open(filename)
    im_width = dataset.RasterXSize
    im_height = dataset.RasterYSize
    im_proj = dataset.GetProjection()
    im_data = dataset.ReadAsArray(0,0,im_width,im_height)
    #print(im_data)
    #del im_data
    return im_data

#读图像文件
def read_tif(filename):
    dataset=gdal.Open(filename) #打开文件
    im_width = dataset.RasterXSize #栅格矩阵的列数
    im_height = dataset.RasterYSize #栅格矩阵的行数
    im_geotrans = dataset.GetGeoTransform() #仿射矩阵
    im_proj = dataset.GetProjection() #地图投影信息
    im_data = dataset.ReadAsArray(0,0,im_width,im_height) #将数据写成数组，对应栅格矩阵
    del dataset #关闭对象，文件dataset
    return im_proj,im_geotrans,im_data,im_width,im_height

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
    #读数据并获取影像信息
    data = read_img('S2_20190727San.tif')
    #data = read_img('MOD021KM.A2019335.0000.061.2019336163422.hdf')
