from PIL import Image
import numpy as np
from numba import njit
import pandas as pd


# image=Image.open('地图.png')
# out = image.convert("RGB")
# img=np.array(out)
@njit(fastmath=True, parallel=True)
def _get_coord(img):
    tar = [[189, 0, 38], [240, 59, 32], [253, 141, 60], [254, 204, 92], [255, 255, 178]]
    coord = [[-1, -1]]
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if [img[i][j][0], img[i][j][1], img[i][j][2]] in tar:
                coord += [[i, j]]
    return coord[1:]


class RGB:
    def __init__(self, path):
        image = Image.open(path)
        out = image.convert("RGB")
        self.img = np.array(out)
        self.coord = _get_coord(self.img)
        self.coord_r = []
        self.cr = [0,0]
        self.cn = 0
        self.cut_off()

    # def __del__(self):
    #     print("del class")

    def cut_off(self):
        if len(self.coord) != 0:
            self.ite(self.coord[0])
            self.coord_r.append([self.cr[0]/self.cn,self.cr[1]/self.cn])
            self.cr = [0,0]
            self.cn = 0
            self.cut_off()


    def ite(self, point):
        p1 = [point[0], point[1] + 1]
        p2 = [point[0], point[1] - 1]
        p3 = [point[0] + 1, point[1] + 1]
        p4 = [point[0] + 1, point[1] - 1]
        p5 = [point[0] - 1, point[1] + 1]
        p6 = [point[0] - 1, point[1] - 1]
        p7 = [point[0] + 1, point[1]]
        p8 = [point[0] - 1, point[1]]
        p9 = [point[0], point[1]]
        if p1 in self.coord:
            self.coord.remove(p1)
            self.cr[0] += p1[0]
            self.cr[1] += p1[1]
            self.cn += 1
            self.ite(p1)
        if p2 in self.coord:
            self.coord.remove(p2)
            self.cr[0] += p2[0]
            self.cr[1] += p2[1]
            self.cn += 1
            self.ite(p2)
        if p3 in self.coord:
            self.coord.remove(p3)
            self.cr[0] += p3[0]
            self.cr[1] += p3[1]
            self.cn += 1
            self.ite(p3)
        if p4 in self.coord:
            self.coord.remove(p4)
            self.cr[0] += p4[0]
            self.cr[1] += p4[1]
            self.cn += 1
            self.ite(p4)
        if p5 in self.coord:
            self.coord.remove(p5)
            self.cr[0] += p5[0]
            self.cr[1] += p5[1]
            self.cn += 1
            self.ite(p5)
        if p6 in self.coord:
            self.coord.remove(p6)
            self.cr[0] += p6[0]
            self.cr[1] += p6[1]
            self.cn += 1
            self.ite(p6)
        if p7 in self.coord:
            self.coord.remove(p7)
            self.cr[0] += p7[0]
            self.cr[1] += p7[1]
            self.cn += 1
            self.ite(p7)
        if p8 in self.coord:
            self.coord.remove(p8)
            self.cr[0] += p8[0]
            self.cr[1] += p8[1]
            self.cn += 1
            self.ite(p8)
        if p9 in self.coord:
            self.coord.remove(p9)
            self.cr[0] += p9[0]
            self.cr[1] += p9[1]
            self.cn += 1
            self.ite(p9)
