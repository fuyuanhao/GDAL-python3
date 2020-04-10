import cv2,os

# 获取工程根目录的路径
rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# 数据文件路径
dataPath = os.path.abspath(rootPath + r'\Image')
# 切换目录
os.chdir(dataPath)
# SHP文件路径
imgFile ="cat.jpg"
# 读取图片并缩放方便显示
img = cv2.imread(imgFile)
height, width = img.shape[:2]
size = (int(width * 0.5), int(height * 0.5))
# 缩放
img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
# BGR转化为HSV
HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
print(img[25,36][1])
print(HSV[25,36])
# 鼠标点击响应事件
def getposHSV(event, x, y, flags, param):
    if event==cv2.EVENT_LBUTTONDOWN:
        print("HSV is", HSV[y, x])

def getposBGR(event, x, y, flags, param):
    if event==cv2.EVENT_LBUTTONDOWN:
        print("BGR is", img[y, x])

cv2.imshow("imageHSV", HSV)
cv2.imshow('imageBGR', img)
cv2.setMouseCallback("imageHSV", getposHSV)
cv2.setMouseCallback("imageBGR", getposBGR)
cv2.waitKey(0)