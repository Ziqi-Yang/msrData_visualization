# MSR 3d Action Data Visualization

Used dataset: [MSRAction3DSkeletonReal3D.rar](https://uowmailedu-my.sharepoint.com/personal/wanqing_uow_edu_au/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fwanqing%5Fuow%5Fedu%5Fau%2FDocuments%2FResearchDatasets%2FMSRAction3D)

## requirements

1. 安装所需要的python库

```shell
pip install -r ./requirements.txt
```

2. 生成动画(`mp4`或者`gif`)所需要的依赖
`ffmpeg`或者`imagemagisk`, 自行搜索安装

## Usage

1. 查看某一文件对应的动画
修改`main.py`最下方的变量`dataPath`为你想查看文件的相对路径,然后执行以下命令
``` python
python main.py
```
2. 对比两文件:
修改`compare.py`最下方的`file1`和`file2`参数,然后运行
```shell
python compare.py
```
---
至于更多自定义需求查看文件里的`genVideo`函数的说明

## 补充

### 数据解释

使用了`MSR 3d action数据集`, 用到的此数据集数据在`msrData`文件夹下  
以文件a01_s01_e01_skeleton3D.txt为例进行说明。该文件共4列1080行。其中，每行存储着每帧骨架关键点的(x, y, z, c)的数据，其中(x,y,z)是以kinect为坐标原点的世界坐标系下的值，c是置信度得分。每个骨架共有20个关键点，因此该文件中共存储1080/20=54帧的关键点数据。骨架关键点的位置，以及第一帧的20个关键点数据如下图所示。
![](./assert/dataExplaination.jpg)
`kinect`坐标系
![](./assert/kinect.jpg)
对应到正常坐标系下
![](./assert/dataExplaination2.png)  
对应关系:  
$$X_{normal} = Z_{msr}$$  
$$Y_{normal} = X_{msr}$$  
$$Z_{normal} = Y_{msr}$$  


