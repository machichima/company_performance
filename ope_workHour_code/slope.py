import pandas as pd
import os
from scipy.stats import linregress

def slope(dataset):
    x_li = []
    y_li = []
    for i, c in enumerate(dataset.columns):
        if(i % 2 == 0):
            if(dataset[c].isnull().sum() >= len(dataset[c])-1):
                continue
            else:
                x_li.append(dataset[c].index)
                y_li.append(dataset.iloc[:, i+1])

    total_slope = 0
    for i, x_val, y_val in zip(range(len(x_li)), x_li, y_li):
        x_val = x_val[y_val.notna()]
        y_val = y_val[y_val.notna()]
        reg_up=linregress(x=x_val.astype(float),y=y_val)
        print(reg_up[0], "total: ", total_slope)
        total_slope += reg_up[0]

    return total_slope