import numpy as np
import pandas as pd

#定义多维数组
df = pd.DataFrame(np.array([[88, 66, 99, 69],[85, 65, 83, 89],
                            [86, 93, 75, 91],[77, 66, 93, 88]]),
                  columns=['GIS', 'AI', 'GPS', 'RS'],
                  index=['A', 'B', 'C', 'D'])
print('--------------输出多维数组-------------------')
print(df)

print('--------------计算df第二行的平均值--------------')
all2mean=df.iloc[1, :].mean() # 计算第二行的平均值
print(all2mean)

print('--------------计算df计算所有行的平均值--------------')
allrowmean=df.mean(axis = 1)# 计算所有行的平均值
print(allrowmean)

print('--------------计算df第三列的平均值--------------')
all3mean=df.iloc[:, 2].mean() # 计算第三列的平均值
print(all3mean)

print('--------------计算df计算所有列的平均值--------------')
allcolummean=df.mean(axis = 0)# 计算所有列的平均值
print(allcolummean)
