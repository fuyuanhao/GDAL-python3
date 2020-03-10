'''
scipy.optimize.leatsq():使用最小二乘法拟合直线
'''
import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

#定义拟合函数形式
def func(p,x):
    k,b = p
    return k*x+b

#定义误差函数
def error(p,x,y,s):
    print(s)
    return func(p,x)-y

#最小二乘拟合函数、制图
def TestLeastsq(p,Xi,Yi):
    #使用leastsq()函数进行参数估计
    s = '参数估计次数'
    Para = leastsq(error,p,args=(Xi,Yi,s))
    #系数与常数项求解
    k,b = Para[0]
    #结果输出
    print('k=',k,'\n','b=',b)
    #图形可视化
    plt.figure(figsize = (8,6))
    #绘制训练数据的散点图
    plt.scatter(Xi,Yi,color='r',label='Sample Point',linewidths = 3)
    #X坐标
    plt.xlabel('x')
    #y坐标
    plt.ylabel('y')
    x = np.linspace(0,2000,1000)
    #函数
    y = k*x+b
    #制图
    plt.plot(x,y,color= 'orange',label = 'Fitting Line',linewidth = 2)
    #图例
    plt.legend()
    #展示图表
    plt.show()

#-----------------以下为函数测试的数据和调用部分--------------------------

#两组训练数据

Xi = np.array([1400.5256,23.46947992,18.765234,0.3400712,1162.1815,2.160179832,573.86017,7.86524803,96.691,6.909166922,0.93668854])
Yi = np.array([1450.4054,5.789398075,21.995316,0.153889867,1174.8822,2.71192977,700.67657,7.167389955,100,0.047114187,0.9755041])
#随机给出参数的初始值
p = [8,3]

#函数调用
TestLeastsq(p,Xi,Yi)