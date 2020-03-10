import numpy as np
from scipy import linalg
A = np.array([[1,3,5],[2,5,1],[2,3,8]])
A_inv = linalg.inv(A)
print(A)
print(A_inv)


