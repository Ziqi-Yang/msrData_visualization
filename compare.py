import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation
import pandas as pd
import numpy as np
import os

# 若需要在图例中显示中文请取消下面两行的注释, 若这样还不行吧下面的第一行的SimHei改为你系统中的中文字体名称
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号



def preProcessData(filePath: str):
    keyPoints = pd.read_csv(filePath, sep=' ', header=None)
    keyPoints.columns = ['x', "y", "z", "c"]
    order = ["z", "x", "y"]
    keyPoints = keyPoints[order]  # 改变顺序和去掉c
    frameNum = keyPoints.shape[0] // 20
    DATA = np.array([np.array(keyPoints.iloc[i * 20:(i + 1) * 20]) for i in range(frameNum)])
    return DATA


def genVideo(filePath1: str, filePath2: str, fmt="gif", showXYZ=False, showLegend=False,
             customLegendPrompt=["file_1", "file_2"]):
    """
    :param filePath1: 对比文件1路径
    :param filePath2: 对比文件2路径
    :param fmt: 生成文件格式,支持gif和mp4
    :param showXYZ: 是否显示坐标轴
    :param showLegend: 是否显示图例
    :param customLegendPrompt: 自定义图例文字
    :return:
    """
    hasChangedOrder = False

    data1 = preProcessData(filePath1)
    data2 = preProcessData(filePath2)
    if data1.shape[0] < data2.shape[0]:
        data1, data2 = data2, data1
        hasChangedOrder = True
    DATA = np.zeros((data1.shape[0], 20, 6))
    for i in range(data2.shape[0]):
        for j in range(20):
            DATA[i, j] = np.append(data1[i, j], data2[i, j])
    for i in range(data2.shape[0], data1.shape[0]):
        for j in range(20):
            DATA[i, j, :3] = data1[i, j]

    divideLength = data2.shape[0]  # 从此位置开始就只有data1数据了[data1_x,data1_y,data1_z,0,0,0]
    dataIndex = 0

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(projection="3d")

    coord_scale = []
    for i in range(3):
        minScale = min(data1[:, :, i].min() - abs(data1[:, :, i].min()) * 0.3,
                       data2[:, :, i].min() - abs(data2[:, :, i].min()) * 0.3)
        maxScale = max(data1[:, :, i].max() + abs(data1[:, :, i].max()) * 0.3,
                       data2[:, :, i].max() + abs(data2[:, :, i].max()) * 0.3)
        coord_scale.append([minScale, maxScale])

    ax.set_xlim3d(*coord_scale[0])
    ax.set_ylim3d(*coord_scale[1])
    ax.set_zlim3d(*coord_scale[2])

    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    if showXYZ:
        ax.set_xlabel("z")
        ax.set_ylabel("x")
        ax.set_zlabel("y")

    if showLegend:
        custom_lengend = [Line2D([0], [0], color="steelblue", lw=4),
                          Line2D([0], [0], color="red", lw=4)]
        customLegendPrompt = customLegendPrompt[::-1] if hasChangedOrder else customLegendPrompt
        ax.legend(custom_lengend, customLegendPrompt)

    draw_sequences = np.array([  # 人体骨骼框架连线
        [11, 9, 7, 0, 2, 1, 8, 10, 12],
        [19, 2, 3, 6],
        [6, 4, 13, 15, 17],
        [6, 5, 14, 16, 18]
    ], dtype=object)

    skeleton1 = [ax.plot([], [], [], c="steelblue", marker="o")[0] for _ in range(len(draw_sequences))]
    skeleton2 = [ax.plot([], [], [], c="red", marker="o")[0] for _ in range(len(draw_sequences))]

    # texts = [ax.text(0, 0, 0, f"{i + 1}") for i in range(20)]

    def update(points):
        nonlocal dataIndex

        index = 0
        for seq in draw_sequences:
            Vertexes = np.array([points[i] for i in seq]).T
            if dataIndex < divideLength:
                skeleton1[index].set_data(Vertexes[:2, :])
                skeleton1[index].set_3d_properties(Vertexes[2, :])

                skeleton2[index].set_data(Vertexes[3:5, :])
                skeleton2[index].set_3d_properties(Vertexes[5, :])
            else:
                skeleton1[index].set_data(Vertexes[:2, :])
                skeleton1[index].set_3d_properties(Vertexes[2, :])
            index += 1

        dataIndex += 1

        # for i in range(20):
        #     x, y, z = points[i]
        #     texts[i].set_x(x)
        #     texts[i].set_y(y)
        #     texts[i].set_z(z)

    # fig.tight_layout()
    exportName = f"compare_result.{fmt}"
    anim = animation.FuncAnimation(fig, update, DATA, interval=40)  # 在interval处修改每帧间隔时间
    anim.save(os.path.join("export", exportName), dpi=300)

    if not showLegend:
        print("设置 showLegend 参数来显示图例")



if __name__ == '__main__':
    file1 = "./msrData/a01_s01_e01_skeleton3D.txt"
    file2 = "./msrData/a01_s01_e02_skeleton3D.txt"
    genVideo(file1, file2, fmt="gif", showLegend=True)
    print("Result file `compare_result` is in the `export` folder.")
