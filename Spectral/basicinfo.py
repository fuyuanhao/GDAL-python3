# -*- coding: utf-8 -*-
from spectral import *
import matplotlib.pyplot as plt
import os

from spectral.io.envi import save_image

def basicinfo(imagepath):
    img = open_image(imagepath)
    print(img)
    print(img.__class__)
    print(img.shape)
    band6 = img[:,:,5]
    pixel = img[49,57,117]
    print(pixel)
    print(band6.shape)

def DisplayData(imagepath):

    img = open_image(imagepath)
    data = img.load()
    print(data)

    #save_image('rgb.png', (data[29, 19, 9]), format='png')
    #view = imshow(img, (29, 19, 9))
    # data = img[0:144,0:144,29]
    # print(data)
    band29 = data.read_band(29)
    print(band29)
    #view = imshow(band120)
    plt.hist(band29)
    plt.title("band29")
    plt.show()
    gt = open_image('92AV3GT.GIS').read_band(0)
    # #view = imshow(classes=gt)
    plt.imshow(gt, cmap='Greys_r')
    plt.colorbar()
    plt.show()

def displayRGB(imagepath):
    img = open_image(imagepath)
    view = imshow(img, (198, 126, 15))
    print(view)
    plt.pause(10)
    #data_norm = np.array([normalize(view[i, :, :], 0, 255) for i in range(view.shape[0])])
    #data_rgb = data_norm.astype("uint8")
    # plt.imshow(view)
    # plt.colorbar()
    # plt.show()

def displayGoundtruth(imagepath):
    img = open_image(imagepath)
    gt = open_image('92AV3GT.GIS').read_band(0)
    view = imshow(classes=gt)
    view = imshow(img, (30, 20, 10), classes=gt)
    view.set_display_mode('overlay')
    view.class_alpha = 0.5
    plt.pause(10)

#主函数
if __name__ == '__main__':
    #获取工程根目录的路径
    rootPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    RdataPath = os.path.abspath(rootPath + r'\SpectralData')
    #切换目录
    os.chdir(RdataPath)
    #测试影像数据
    imagepath ='92AV3C.lan'
    #basicinfo(imagepath)
    #displayRGB(imagepath)
    displayGoundtruth(imagepath)