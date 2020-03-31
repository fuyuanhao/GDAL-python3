# _*_ coding: utf-8 _*_
# 导入geopandas
import geopandas,os
import matplotlib.pyplot as plt
from geopandas import GeoSeries

# 用来正常显示中文标签
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['figure.dpi'] = 200 #分辨率

#利用geopandas打开shp数据并绘图
def showShp(shpfilename):

    # 创建空间数据
    gdf = geopandas.GeoDataFrame

    # 读取SHP文件
    shp = gdf.from_file(shpfilename, encoding='gb18030')
    g = GeoSeries(shp['geometry'])
    buffer = g.buffer(0.001)
    print(shp.head())  #输出属性表

    #fig, ax = plt.subplots(figsize=(8, 6))
    # Shp文件绘图
    ax=shp.geometry.plot(alpha=0.5, facecolor='red',label='KFC')

    ax=buffer.geometry.plot(ax=ax,alpha=0.5, facecolor='white',edgecolor='blue')
    # 单独提前设置图例标题大小
    plt.rcParams['legend.title_fontsize'] = 14
    plt.legend(title="图例", loc='lower left', ncol=1, shadow=True)
    #plt.axis('off') # 不显示坐标轴
    #plt.grid(True)

    plt.show()

def Rectanglelegend():
    fig = plt.figure()#创建图
    ax = fig.add_subplot(111)  #创建子图

    rect1 = plt.Rectangle((0.1,0.1),0.5,0.3,facecolor='red')
    rect2 = plt.Rectangle((0.2,0.2),0.5,0.3)
    ax.add_patch(rect1)
    ax.add_patch(rect2)
    #plt.gca().add_patch(plt.Rectangle((0.1,0.1),0.5,0.3))
    plt.gca().legend((rect1,rect2),('长方形1','长方形2'))
    plt.show()

def showtwopoint(shp_a,shp_b):
    df_a = geopandas.read_file(shp_a)
    #print(df_a)
    df_b = geopandas.read_file(shp_b)
    print(df_b)
    #ax = df_a.plot(color='red',label='餐饮')
    #bx=df_b.plot(ax=ax, color='green', alpha=0.5,label='风景名胜')
    base = df_a.plot(color='coral', markersize = 2, label='餐饮')
    df_b.plot(ax=base, marker='*', color='lawngreen', markersize=3, alpha=0.5, label = '风景名胜')
    plt.legend(title="图例", loc='best', ncol=1, shadow=True)
    plt.rcParams['legend.title_fontsize'] = 10

    plt.show()

#主函数
if __name__ == '__main__':

    # 获取工程根目录的路径
    rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    #print('rootPath:'+rootPath)
    # 数据文件路径
    dataPath = os.path.abspath(rootPath + r'\ShpData')
    #print('dataPath:'+dataPath)
    # 切换目录
    os.chdir(dataPath)

    # SHP文件路径
    #strVectorFile ="KFC.shp"
    #showShp(strVectorFile)
    #Rectanglelegend()
    shp_a="canyin.shp"
    shp_b='fengjing.shp'
    showtwopoint(shp_a,shp_b)