import numpy as np
import pandas as pd

df = pd.DataFrame({"A":[1, 2, 3],"B":[2, 5, 6]}, index=['a', 'b', 'c'])
print("-----原始数据格式-----")
print(df)
print("-----JSON数据格式-----")
print(df.to_json())
print("-----CSV数据格式-----")
print(df.to_csv())