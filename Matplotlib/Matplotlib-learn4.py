"""
matplotlib.pyplot read and show picture.
"""
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

#用来正常显示中文标签
plt.rcParams['font.sans-serif']=['SimHei']
#打开指定图片
image = plt.imread('wh.jpg')
#定义图片框
plt.figure()
# 将画板分为2行两列，本幅图位于第一个位置
plt.subplot(2,2,1)
plt.title("原始图片")
#图片显示原始图像
plt.imshow(image)

# 将画板分为2行两列，本幅图位于第二个位置
plt.subplot(2,2,2)
plt.title("红色通道")
#指定图片中的红波段
im_r = image[:, :, 0]  # 红色通道
#图片显示红波段
plt.imshow(im_r)

# 将画板分为2行两列，本幅图位于第3个位置
plt.subplot(2,2,3)
plt.title("灰度图")
# 加载灰度图，可以添加 cmap 参数解决
plt.imshow(im_r, cmap='Greys_r')

#窗口中展示图片
plt.show()

