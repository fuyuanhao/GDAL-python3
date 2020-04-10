# -*- coding: utf-8 -*-
import fiona
import numpy as np
import matplotlib.pyplot as plt
import os
import rasterio
import rasterio.mask
from rasterio.plot import show, show_hist
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio import crs
from rasterio.enums import Resampling
import cv2

from matplotlib import colors


class MidpointNormalize(colors.Normalize):

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))

#获取栅格数据基本信息
def getTIFFInfo(imagepath):
    with rasterio.open(imagepath) as ds:

        print(f'数据格式：{ds.driver}')
        print(f'波段数目：{ds.count}')
        print(f'影像宽度：{ds.width}')
        print(f'影像高度：{ds.height}')
        print(f'地理范围：{ds.bounds}')
        print(f'反射变换参数（六参数模型）：\n {ds.transform}')
        print(f'投影定义：{ds.crs}')
        # show_hist(ds, bins=50, lw=0.0, stacked=False,
        #           alpha=0.3,histtype='stepfilled',
        #           title="Histogram")
        num_bands= ds.count
        print('波段数为：'+str(num_bands))
        for index in range(num_bands):
            band=index+1
            show((ds,band),cmap='Greys_r')
            #plt.hist(ds.read(band))
            #plt.title("band"+str(band))
            plt.show()

def normalize(x, lower, upper):
    """Normalize an array to a given bound interval"""

    x_max = np.max(x)
    x_min = np.min(x)

    m = (upper - lower) / (x_max - x_min)
    x_norm = (m * (x - x_min)) + lower

    return x_norm

def showTiFF(imagepath):
    with rasterio.open(imagepath) as ds:
        print(ds.profile)
        if(ds.count > 3):
            ds = ds.read([1,2,3])
            data_norm = np.array([normalize(ds[i, :, :], 0, 255) for i in range(ds.shape[0])])
            data_rgb = data_norm.astype("uint8")
            #show(ds.read([1, 2, 3]).astype('uint8'))
            show(data_rgb)
        #show(ds)
        # show_hist(ds, bins=50, lw=0.0, stacked=False,
        #           alpha=0.3,histtype='stepfilled',
        #           title="Histogram")

def linearstretching(img,min,max):

    img=np.where(img > min, img, min)
    img=np.where(img < max, img, max)
    img = (img - min) / (max - min) * 255
    return img


#获取影像的指定波段
def getBand(imagepath,bandnum):
    with rasterio.open(imagepath) as ds:
        if(bandnum in len(ds.count)):
            band = ds.read(bandnum)
    return band
    ds.close()

#栅格转投影
#参考博客：https://blog.csdn.net/theonegis/article/details/80663218
#官方参考：https://www.osgeo.cn/rasterio/topics/reproject.html
def TransferRasterProject(src_img,epsg_name):

    dst_crs = crs.CRS.from_epsg(epsg_name) #目标投影
    with rasterio.open(src_img) as src_ds: #打开输入影像
        profile = src_ds.profile #获取输入影像的基本信息
        print(src_ds.profile)
        # 计算在新空间参考系下的仿射变换参数，图像行列数
        dst_transform, dst_width, dst_height = calculate_default_transform(
            src_ds.crs, dst_crs, src_ds.width, src_ds.height, *src_ds.bounds)

        # 更新数据集的元数据信息
        profile.update({
            'crs': dst_crs, #目标投影信息
            'transform': dst_transform, #仿射变换参数
            'width': dst_width, #列
            'height': dst_height, #高
            'nodata': 0 #无效值赋值为0
        })

        shorFilename = src_img.split('.')[0] #获取文件名【不包含后缀名】
        dst_img= shorFilename+"_"+epsg_name+".tif" #组装输出的clip栅格文件名
        print('dst_img:'+dst_img)

        # 重投影并输出数据
        with rasterio.open(dst_img, 'w', **profile) as dst_ds:
            band = src_ds.count+1
            for i in range(1, band): #波段从1开始计数
                src_array = src_ds.read(i) # 读取各波段数据
                dst_array = np.empty((dst_height, dst_width), dtype=profile['dtype']) #数据类型
                reproject( #重投影
                    # 源文件参数
                    source=src_array, #数据源
                    src_crs=src_ds.crs, #投影坐标系
                    src_transform=src_ds.transform, #仿射变换参数
                    # 目标文件参数
                    destination=dst_array,
                    dst_transform=dst_transform,
                    dst_crs=dst_crs,
                    # 其它配置
                    resampling=Resampling.cubic, #三次卷积重采样
                    num_threads=2)

                dst_ds.write(dst_array, i)#写数据
    showTiFF(dst_img)

#矢量裁剪栅格
def TIF_ClipbyShp(TIFFile,shpFile):

    #打开矢量文件，r为read,读数据
    with fiona.open(shpFile, "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]#获取几何信息

    #打开被裁剪栅格
    with rasterio.open(TIFFile) as src:
        #showTiFF(TIFFile)
        #crop=True，按照矢量多边形的形状来裁剪影像,mask掩膜处理，这里注意，要import rasterio.mask
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta #输入栅格的元数据赋值给输出影像
        out_meta.update({"driver": "GTiff", #数据驱动类型，GTiff
                         "height": out_image.shape[1], #行
                         "width": out_image.shape[2], #列
                         "transform": out_transform}) #反射变换参数

    shorFilename = TIFFile.split('.')[0] #获取文件名【不包含后缀名】
    out_TIFF= shorFilename+"_clip.tif" #组装输出的clip栅格文件名
    print('out_TIFF:'+out_TIFF)
    #输出裁剪后栅格，w为write，写
    with rasterio.open(out_TIFF, "w", **out_meta) as dest:
        dest.write(out_image) #输出裁剪后的影像数据
    showTiFF(out_TIFF)

# 计算NDVI
def calcNDVI(TIFFile):
    # # 打开被裁剪栅格
    # with rasterio.open(TIFFile) as src:
    #     showTiFF(TIFFile)
    #     #raster = src.read()  # 读取所有波段
    #     red = src.read(3)
    #     nir = src.read(4)
    #     #  源数据的元信息集合（使用字典结构存储了数据格式，数据类型，数据尺寸，投影定义，仿射变换参数等信息）
    #     profile = src.profile
    #     shorFilename = TIFFile.split('.')[0] #获取文件名【不包含后缀名】
    #     out_TIFF= shorFilename+"_NDVI.tif" #组装输出的clip栅格文件名
    #     print('out_TIFF:'+out_TIFF)
    #     # 计算NDVI指数（对除0做特殊处理）
    #     with np.errstate(divide='ignore', invalid='ignore'):
    #         ndvi = (nir - red) / (nir + red+0.00001)
    #         ndvi[ndvi == np.inf] = 0
    #         ndvi = np.nan_to_num(ndvi)  # 写入数据
    #         profile.update(dtype=ndvi.dtype, count=1)
    #     with rasterio.open(out_TIFF, mode='w', **profile) as dst:
    #         dst.write(ndvi, 1)
    #     show(ndvi,cmap='Greys_r')
    with rasterio.open(TIFFile) as src:
        band_red = src.read(3)
    with rasterio.open(TIFFile) as src:
        band_nir = src.read(4)
    # Do not display error when divided by zero

    np.seterr(divide='ignore', invalid='ignore')

    # NDVI
    ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)
    print(np.nanmin(ndvi))
    print(np.nanmax(ndvi))
    # get the metadata of original GeoTIFF:
    meta = src.meta
    print(meta)

    # get the dtype of our NDVI array:
    ndvi_dtype = ndvi.dtype
    print(ndvi_dtype)

    # set the source metadata as kwargs we'll use to write the new data:
    kwargs = meta

    # update the 'dtype' value to match our NDVI array's dtype:
    kwargs.update(dtype=ndvi_dtype)

    # update the 'count' value since our output will no longer be a 4-band image:
    kwargs.update(count=1)

    # Finally, use rasterio to write new raster file 'data/ndvi.tif':
    with rasterio.open('ndvi.tif', 'w', **kwargs) as dst:
        dst.write(ndvi, 1)
    # Set min/max values from NDVI range for image

    min = np.nanmin(ndvi)
    max = np.nanmax(ndvi)

    # Set our custom midpoint for most effective NDVI analysis
    mid = 0.1

    # Setting color scheme ref:https://matplotlib.org/users/colormaps.html as a reference
    colormap = plt.cm.RdYlGn
    norm = MidpointNormalize(vmin=min, vmax=max, midpoint=mid)
    fig = plt.figure(figsize=(20, 10))

    ax = fig.add_subplot(111)

    # Use 'imshow' to specify the input data, colormap, min, max, and norm for the colorbar
    cbar_plot = ax.imshow(ndvi, cmap=colormap, vmin=min, vmax=max, norm=norm)

    # Turn off the display of axis labels
    ax.axis('off')

    # Set a title
    ax.set_title('Normalized Difference Vegetation Index', fontsize=17, fontweight='bold')

    # Configure the colorbar
    cbar = fig.colorbar(cbar_plot, orientation='horizontal', shrink=0.65)

    # Call 'savefig' to save this plot to an image file
    fig.savefig("ndvi-image.png", dpi=200, bbox_inches='tight', pad_inches=0.7)

    # let's visualize
    plt.show()

#主函数
if __name__ == '__main__':
    # 获取工程根目录的路径
    rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # 矢量数据文件路径
    ShpdataPath = os.path.abspath(rootPath + r'\ShpData')
    shpfile =ShpdataPath + r'\border.shp'
    # 栅格数据文件路径
    RdataPath = os.path.abspath(rootPath + r'\RasterData')
    # 切换目录
    os.chdir(RdataPath)
    # 测试影像数据
    #imagepath ='wh_20200320_B2348.tif'
    #imagepath = 'wh_20200320_B2348_4326.tif'
    imagepath = 'wh_20200320_B2348_clip.tif'
    #getTIFFInfo(imagepath)
    #showTiFF(imagepath)

    #TIF_ClipbyShp(imagepath,shpfile)
    #TransferRasterProject(imagepath,"4326")
    #TIF_Resample(imagepath,1/2)
    calcNDVI(imagepath)
    #getsubdata(imagepath,3000)
