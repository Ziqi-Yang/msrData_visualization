import pandas as pd     #引入pandas包
import numpy as np
import matplotlib.pyplot as plt


keypoint=pd.read_csv('./msrData/a01_s01_e01_skeleton3D.txt',sep='\t',header=None)     #读入txt文件，分隔符为\t

keypoint.columns=['x']
keypoint['y']=None
keypoint['z']=None
keypoint['c']=None

for i in range(len(keypoint)):         #遍历每一行
    coordinate = keypoint['x'][i].split() #分开第i行，u列的数据。split()默认是以空格等符号来分割，返回一个列表
    keypoint['x'][i]=float(coordinate[0])       #分割形成的列表第一个数据给u列
    keypoint['y'][i]=float(coordinate[1])        #分割形成的列表第二个数据给v列
    keypoint['z'][i]=float(coordinate[2])        #分割形成的列表第一个数据给d列
    keypoint['c'][i]=float(coordinate[3])        #分割形成的列表第二个数据给c列
print(keypoint)

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
pointx = keypoint['x'].values
pointy = keypoint['y'].values
pointz = keypoint['z'].values
plt.ion()
fig = plt.figure()
ax = Axes3D(fig)
for i in range(80):
    plt.cla()
    ax.scatter(pointz[20*(i-1):20*i], pointx[20*(i-1):20*i], pointy[20*(i-1):20*i])
    ax.set_xlim(0, 5)
    ax.set_ylim(-1, 1)

    # 添加坐标轴(顺序是Z, Y, X)
    ax.set_zlabel('Z', fontdict={'size': 15, 'color': 'red'})
    ax.set_ylabel('Y', fontdict={'size': 15, 'color': 'red'})
    ax.set_xlabel('X', fontdict={'size': 15, 'color': 'red'})
    plt.pause(0.1)