import os,geopandas

def shpReproject(strVectorFile):
    vector = geopandas.read_file(strVectorFile)
    print(vector.crs)
    vector_utm = vector.to_crs("epsg:32649")
    print(vector_utm.crs)

# 主函数
if __name__ == '__main__':
    rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    dataPath = os.path.abspath(rootPath + r'\ShpData')
    os.chdir(dataPath)
    strVectorFile ="canyin.shp"
    shpReproject(strVectorFile)

