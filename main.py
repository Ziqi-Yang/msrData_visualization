import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy as np
import sys
import os


def genVideo(dataPath: str, fmt="gif", showXYZ=False, showSkeletonPointsNum=False):
    """
    :param dataPath: 数据文件路径
    :param fmt: 生成文件格式(支持gif和mp4)
    :param showXYZ: 是否显示坐标轴
    :param showSkeletonPointsNum: 是否显示骨骼坐标点的序号
    :return:
    """

    fName = "".join(os.path.basename(dataPath).split(".")[:-1])
    exportName = fName + f".{fmt}"

    keyPoints = pd.read_csv(dataPath, sep=' ', header=None)
    keyPoints.columns = ['x', "y", "z", "c"]
    order = ["z", "x", "y"]
    keyPoints = keyPoints[order]  # 改变顺序和去掉c

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(projection="3d")

    frameNum = keyPoints.shape[0] // 20

    DATA = np.array([np.array(keyPoints.iloc[i * 20:(i + 1) * 20]) for i in range(frameNum)])

    coord_scale = []
    for i in range(3):
        tmp = [DATA[:, :, i].min() - abs(DATA[:, :, i].min()) * 0.3,
               DATA[:, :, i].max() + abs(DATA[:, :, i].max()) * 0.3]
        coord_scale.append(tmp)

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

    draw_sequences = np.array([  # 人体骨骼框架连线
        [11, 9, 7, 0, 2, 1, 8, 10, 12],
        [19, 2, 3, 6],
        [6, 4, 13, 15, 17],
        [6, 5, 14, 16, 18]
    ], dtype=object)

    lines = [ax.plot([], [], [], c="steelblue", marker="o")[0] for _ in range(len(draw_sequences))]
    if showSkeletonPointsNum:
        texts = [ax.text(0, 0, 0, f"{i + 1}") for i in range(20)]

    def update(points):
        index = 0
        for seq in draw_sequences:
            Vertexes = np.array([points[i] for i in seq]).T
            lines[index].set_data(Vertexes[:2, :])
            lines[index].set_3d_properties(Vertexes[2, :])
            index += 1

        if showSkeletonPointsNum:
            for i in range(20):
                x, y, z = points[i]
                texts[i].set_x(x)
                texts[i].set_y(y)
                texts[i].set_z(z)

    # fig.tight_layout()
    anim = animation.FuncAnimation(fig, update, DATA, interval=40)  # 在interval处修改每帧间隔时间
    anim.save(os.path.join("export", exportName), dpi=300)


if __name__ == '__main__':
    dataPath = "./msrData/a01_s01_e01_skeleton3D.txt"
    genVideo(dataPath, fmt="gif")
    print("Result file is in the `export` folder.")
