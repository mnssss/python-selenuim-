import cv2  ## 安装opencv-python
import numpy as np
import easyocr

class CV:
    # def __init__(self, data):
    #     self.img_rgb = cv2.imread(data)

    def match_pic(self, path0, img_rgb):
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) # 完整图片
        template = cv2.imread(path0, 0) # 目标
        h, w = template.shape[:2]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        # 取匹配程度大于%80的坐标
        loc = np.where(res >= threshold)
        sumx = 0
        sumy = 0
        n = 0
        loc_list = []
        # 提取单连通样点
        for i in range(len(loc[0])):
            if i != 0 and loc[0][i] - loc[0][i - 1] in [-1, 0, 1] and loc[1][i] - loc[1][i - 1] in [-1, 0, 1]:
                sumx += loc[1][i]
                sumy += loc[0][i]
                n += 1
            elif i != 0 and not (loc[0][i] - loc[0][i - 1] in [-1, 0, 1] and loc[1][i] - loc[1][i - 1] in [-1, 0, 1]):
                loc_list.append([round(sumx / n), round(sumy / n)])
                sumx = 0
                sumy = 0
                n = 0
                sumx += loc[1][i]
                sumy += loc[0][i]
                n += 1
                continue
            elif i == 0:
                sumx += loc[1][i]
                sumy += loc[0][i]
                n += 1
            else:
                pass
            if i == len(loc[0]) - 1:
                loc_list.append([round(sumx / n), round(sumy / n)])
                sumx = 0
                sumy = 0
                n = 0

        loc_arr = np.array(loc_list)
        if len(loc_arr) != 0:
            # 左上角挂点向目标中心偏移
            loc_arr[:, 0] += round(w / 2)
            loc_arr[:, 1] += round(h / 2)
            # np.where返回的坐标值(x,y)  是(h,w)，注意h,w的顺序
            # 打印图片
            # for pt in loc_arr:
            #     bottom_right = (pt[0] + w, pt[1] + h)
            #     cv2.rectangle(self.img_rgb, pt, bottom_right, (0, 0, 255), 2)
            # cv2.namedWindow('img_rgb', 0)
            # cv2.imshow('img_rgb', self.img_rgb)
            # cv2.waitKey(0)
        return loc_arr.tolist()

    # ocr shibei
    def get_text(self,reader,data):
        result = reader.readtext(data) #,allowlist ='0123456789'限制数字
        result.sort(key=lambda x: x[-1], reverse=True)
        return result
