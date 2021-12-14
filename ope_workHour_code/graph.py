import pandas as pd
import numpy as np
import io
from openpyxl import load_workbook
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from mpl_toolkits.mplot3d.axes3d import Axes3D
import matplotlib.pyplot as plt
import random

def cc(arg):
    return mcolors.to_rgba(arg, alpha=0.6)

def graph_3D(dataset, img_count):

    x_li = []
    z_li = []
    dataset_dropEmp = dataset
    for i, c in enumerate(dataset.columns):
        if(i % 2 == 0):
            if(dataset[c].isnull().sum() >= len(dataset[c])-5):
                dataset_dropEmp = dataset.drop(dataset.columns[[i, i+1]], axis=1)
            else:
                x_li.append(dataset[c].index)
                z_li.append(dataset.iloc[:, i+1])

    fig, ax = plt.subplots(subplot_kw={'projection': '3d'}, figsize=(20, 10))

    #ax.axis('auto')

    #datasets = [{"x":[1,2,3], "y":[i, i+1, i+2], "z":[1, 1, 1], "colour": "red"} for i in range(6)]



    for c, x, z in zip(range(1, len(x_li)+1), x_li, z_li):
        r = random.uniform(0, 0.7)
        b = random.uniform(0, 0.7)
        g = random.uniform(0, 0.7)
        color = (r, g, b)
        ax.plot(x, [c*2]*len(x), z, color=color)

    ax.get_xticks()

    # for dataset in datasets:
    #     ax.plot(dataset["x"], dataset["y"], dataset["z"], color=dataset["colour"])

    ax.view_init(30, 120)
    ax.set_ylim(1, len(x_li)*2)

    x_scale=1#0.75
    y_scale=1.5
    z_scale=1

    scale=np.diag([x_scale, y_scale, z_scale, 1.0])
    scale=scale*(1.0/scale.max()) 
    scale[3,3]=1.0

    def short_proj():
        return np.dot(Axes3D.get_proj(ax), scale)

    ax.get_proj=short_proj
    ax.set_position([0, 10, 12, 1])

    #set_axes_equal(ax)
    #plt.show()

    # bytes_image = io.BytesIO()
    # plt.savefig(bytes_image, format='png')
    # bytes_image.seek(0)
    # return bytes_image
    plt.savefig("./static/images/"+str(img_count)+".png", bbox_inches='tight',orientation='landscape', facecolor='white', edgecolor='none')
