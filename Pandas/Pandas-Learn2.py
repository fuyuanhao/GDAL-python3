# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

#方法一：默认读取第一个表单
def readExcelbyFileName(filename):
    #这个会直接默认读取到这个Excel的第一个表单
    df=pd.read_excel(filename)
    data=df.head()#默认读取前5行的数据
    print("获取到所有的值:\n{0}".format(data))#格式化输出
    #读取第1行到第4行，第1列到第22列的值，包括表头
    data=df.iloc[0:3,:]
    print("读取指定行的数据：\n{0}".format(data))#格式化输出
    return data

#方法二：通过指定表单名的方式来读取
def readExcelbyFileNameAndSheetName(filename,sheetname):
    #可以通过sheet_name来指定读取的表单
    df=pd.read_excel(filename,sheet_name=sheetname)
    print("输出列标题",df.columns.values)
    data=df.values#读取全部数据
    print("获取到所有的值:\n{0}".format(data))#格式化输出
    return data

#测试
filename='ProvinceFruit_1999_2018.xlsx'
#方法一调用
data=readExcelbyFileName(filename)
print('--------------计算df计算所有行的平均值--------------')
allrowmean=data.mean(axis = 1)# 计算所有行的平均值
print(allrowmean)

#sheet名称
sheetname = '分省年度数据'
#读取指定文件名和sheet的数据列表
#readExcelbyFileNameAndSheetName(filename,sheetname)
