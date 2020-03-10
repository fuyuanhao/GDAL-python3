import numpy as np
import scipy.stats as st
a = np.array([39, 99, 27, 19, 55])
# 计算偏度
print(st.skew(a))
# 计算峰度
print(st.kurtosis(a))
