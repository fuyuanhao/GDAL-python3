import cv2,os

# 获取工程根目录的路径
rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# 数据文件路径
dataPath = os.path.abspath(rootPath + r'\Image')
# 切换目录
os.chdir(dataPath)
# SHP文件路径
imgFile ="wh_20200320_B2348_clip_NDVI.tif"
# 读取图片并缩放方便显示
img = cv2.imread(imgFile)
print(img.profile)
# height, width = img.shape[:2]
# size = (int(width * 0.5), int(height * 0.5))
# # 缩放
# img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
#
# # 鼠标点击响应事件
# def getposGray(event, x, y, flags, param):
#     if event==cv2.EVENT_LBUTTONDOWN:
#         print("BGR is", img[y, x])
#
# cv2.imshow('imageBGR', img)
# cv2.setMouseCallback("imageBGR", getposGray)
# cv2.waitKey(0)