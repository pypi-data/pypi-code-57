import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot3(input0=None, input1=None, input2=None, s=None, alpha=None, c=None, cmap=None, gif=False, path=None,
          size_x=9, size_y=9, label=False):
    """
    :param input0:
    :param input1:
    :param input2:
    :param s:
    :param alpha:
    :param c:
    :param cmap:
    :param gif:
    :param path:
    :param size_x:
    :param size_y:
    :param label:
    :return:
    """
    if gif:
        if path is None:
            raise Exception("NEED A PATH")
        os.mkdir(path)

    fig = plt.figure(figsize=(size_x, size_y))
    ax = fig.add_subplot(111, projection='3d')

    cm = plt.get_cmap(cmap)
    if s is None:
        s = 20
    if c is None:
        if input1 is None:
            c = input0[:, 2]
        else:
            c = input2

    if label:
        unique_labels = set(c)
        if input1 is None:
            for el in unique_labels:
                xyz = input0[c == el]
                ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], c=("C" + str(el) if el != -1 else "black"), s=s,
                           alpha=alpha,
                           label="# : " + str(len(xyz)) + ", sort : " + str(el))
                ax.legend()
        else:
            for el in unique_labels:
                ax.scatter(input0[c == el][:, 0], input1[c == el][:, 1], input2[c == el][:, 2],
                           c=("C" + str(el) if el != -1 else "black"), s=s,
                           alpha=alpha,
                           label="# : " + str(len(input0[c == el])) + ", sort :" + str(el))
                ax.legend()

    else:
        if input1 is None:
            print("here")
            ax.scatter(input0[:, 0], input0[:, 1], input0[:, 2],
                       alpha=alpha, c=c, s=s)
        else:
            ax.scatter(input0, input1, input2, alpha=alpha, c=c, s=s, cmap=cm)

    if gif:
        import numpy as np
        def temp(angle):
            ax.view_init(elev=90 * np.sin((angle / 180)
                                          * np.pi), azim=angle / 10)
            plt.savefig(path + "/" + '{0:0>5}'.format(angle) + ".png")

        print("making images...", end='')
        for el in range(0, 3600, 20):
            temp(el)
        print("done")

        rel_file_list = os.listdir(path)
        images = []
        rel_file_list.sort()
        import imageio
        for each_file in rel_file_list:
            images.append(imageio.imread(path + "/" + each_file))
        print("making gif...", end='')
        imageio.mimsave(path + "/result.gif", images)
        print("done.")

    else:
        if path is None:
            plt.show()
        else:
            plt.savefig(path)
            plt.close()


def plot2(input0=None, input1=None, s=None, alpha=None, c=None, path=None, size_x=9, size_y=9,
          label=False):
    """
    :param input0:
    :param input1:
    :param s:
    :param alpha:
    :param c: It should be numpy if label is True
    :param path:
    :param size_x:
    :param size_y:
    :param label:
    :return:
    """
    fig, ax = plt.subplots(figsize=(size_x, size_y))

    if s is None:
        s = 20

    if label:
        unique_labels = set(c)
        if input1 is None:
            for el in unique_labels:
                xyz = input0[c == el]
                ax.scatter(xyz[:, 0], xyz[:, 1], c=("C" + str(el) if el != -1 else "black"), s=s, alpha=alpha,
                           label="# : " + str(len(xyz)) + ", sort : " + str(el))
                ax.legend()
        else:
            for el in unique_labels:
                ax.scatter(input0[c == el][:, 0], input1[c == el][:, 1], c=("C" + str(el) if el != -1 else "black"),
                           s=s, alpha=alpha, label="# : " + str(len(input0[c == el])) + ", sort :" + str(el))
                ax.legend()

    else:
        if input1 is None:
            print("here")
            ax.scatter(input0[:, 0], input0[:, 1], alpha=alpha, c=c, s=s)
        else:
            ax.scatter(input0, input1, alpha=alpha, c=c, s=s)

    if path is None:
        plt.show()
    else:
        plt.savefig(path)
        plt.close()
