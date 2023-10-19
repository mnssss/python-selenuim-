# -*- coding: utf-8 -*-
# Author: mn
# Date: 2023-02-05 10:19:12
# LastEditTime: 2023-02-05 10:19:12
# LastEditors: mn
# FilePath: /nfswork/code/MysqlManager.py
import io

import parsel
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  ###get阻塞
import undetected_chromedriver as uc
import time
import config
from selenium import webdriver
import MysqlManager as MY
from random import choice, random
import requests
import HitCoding as hc
import os
import cv2
import numpy as np

import base64
import os
import re
from io import BytesIO
from PIL import Image

js = "let c = document.createElement('canvas');" \
     "let ctx = c.getContext('2d');" \
     "let img = document.getElementsByTagName('img')[0]; /*找到图片*/ " \
     "img.crossOrigin = 'Anonymous';" \
     "c.height=img.naturalHeight;c.width=img.naturalWidth;" \
     "ctx.fillStyle = '#e5e5e5';" \
     "ctx.fillRect(0, 0, c.width, c.height);" \
     "ctx.drawImage(img, 0, 0,img.naturalWidth, img.naturalHeight);" \
     "let base64String = c.toDataURL();return base64String;"


def opendriver():  ####获取driver
    header = choice(config.Chrome())
    # desired_capabilities = DesiredCapabilities.CHROME
    # desired_capabilities["pageLoadStrategy"] = "none"  ####get禁止阻塞
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--start-maximized') # 最大化
    chrome_options.add_argument('user-agent="%s"' % header)
    driver = uc.Chrome(executable_path="chromedriver", options=chrome_options)
    return driver

# 滑块坐标
def site_to_site(star, end) -> list:
    # SITENUM = 0
    # site = []
    # for i in range(SITENUM):
    #     site.append([star[0]+(end[0]-star[0])*random()/2, star[1]+(end[1]-star[1])*random()/2])
    # site.append(end)
    # print(site)
    return [end]


def getimage(driver,num):###获取验证码图并验证
    page = driver.page_source
    selector = parsel.Selector(text=page)
    menu = driver.find_element(*(By.CSS_SELECTOR, '#J_CheckCode'))
    im = menu.screenshot_as_png
    if im != '':
        print('开始识别')
        yy_axes = hc.security_axes(im)
        pic_id = yy_axes['pic_id']
        axes = yy_axes['pic_str']
        print(yy_axes)
        ### 输入文本
        menu = driver.find_element(*(By.CSS_SELECTOR, '#J_LicenceCheckPop > form > div:nth-child(4) > input[type=text]'))  ##找位置
        menu.clear()  # 清除文本框内容
        menu.send_keys(axes)  # 输入
        ## 点击确认
        menu = driver.find_element(*(By.CSS_SELECTOR, '#J_LicenceCheckPop > form > button'))
        ActionChains(driver).click(menu).perform()
        # if wait(driver,'根据相关法律法规要求，经营者相关资质信息公示如下:',2,0.5):
        #     pass
        # else:
        #     hc.ReportError_axes(pic_id)
        #     getimage(driver)
        if WaitCount(driver, 'data:image/png;', 1, 10, 1):
            with open(f'taobao4#/{axes}#{num}.png', 'wb') as f:
                f.write(im)
            pass
        else:
            print('识别失败，重新识别')
            hc.ReportError_axes(pic_id)
            getimage(driver,num)


def match_pic(path0, img_rgb):  #img_rgb np
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(path0, 0)
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    # 取匹配程度大于%80的坐标
    loc = np.where(res >= threshold)
    if len(loc[0]) == 0:
        return 0
    else:
        return 1


def Hitimage(driver,num):###获取验证码图并匹配素材
    page = driver.page_source
    selector = parsel.Selector(text=page)
    menu = driver.find_element(*(By.CSS_SELECTOR, '#J_CheckCode'))
    im = menu.screenshot_as_png
    im_np = cv2.imdecode(np.frombuffer(im, np.uint8), -1)
    if im != '':
        for root, dirs, files in os.walk('taobao4#'):
            for i in files:
                if match_pic(f'taobao4#/{i}',im_np):
                    axes = i.split(".")[0]
                    ### 输入文本
                    menu = driver.find_element(*(By.CSS_SELECTOR, '#J_LicenceCheckPop > form > div:nth-child(4) > input[type=text]'))  ##找位置
                    menu.clear()  # 清除文本框内容
                    menu.send_keys(axes)  # 输入
                    ## 点击确认
                    menu = driver.find_element(*(By.CSS_SELECTOR, '#J_LicenceCheckPop > form > button'))
                    ActionChains(driver).click(menu).perform()
                    # if wait(driver,'根据相关法律法规要求，经营者相关资质信息公示如下:',2,0.5):
                    #     pass
                    # else:
                    #     hc.ReportError_axes(pic_id)
                    #     getimage(driver)
                    if WaitCount(driver, 'data:image/png;', 1, 5, 1):
                        return 0
        with open(f'taobao4#/#{num}.png', 'wb') as f:
            f.write(im)
        print('识别失败，重新识别')
        Hitimage(driver, num)


# 滑块
# star=[-130,0]
# end=[130,0]
def slide(driver,css,star,end):
    # 判断是否是滑块
    if wait(driver,css[5],2,1):
        pass
    else:
        return 0
    # 判断是否是滑块正常状态
    if waitcss(driver,css,1,1):
        menu = driver.find_element(*(By.CSS_SELECTOR, css[3]))
        ActionChains(driver).move_to_element_with_offset(menu, star[0], star[1]).click_and_hold().perform()
        for i in site_to_site(star, end):
            ActionChains(driver).move_to_element_with_offset(menu, i[0], i[1]).perform()
        ActionChains(driver).pause(1).release().perform()
        try:
            WebDriverWait(driver, 2, 0.1).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                  '#J_ShowLicence')))
        except:
            slide(driver, css, star, end)
    else:
        ActionChains(driver).release().perform()
        driver.refresh()
        slide(driver, css, star, end)



# 强制等待字符
def wait(driver, keywords, long, size):
    i = 0
    while i <= long:
        page = driver.page_source
        if page.find(keywords) != -1:
            return 1
        time.sleep(size)
        i += size
    return 0


# 强制等待字符
def WaitCount(driver, keywords, num, long, size):
    i = 0
    while i <= long:
        page = driver.page_source
        if page.count(keywords) >= num:
            return 1
        time.sleep(size)
        i += size
    return 0


# 等待刷新
def waitrefresh(driver, keywords, long, size):
    i = 0
    while i <= long:
        driver.refresh()
        try:
            if wait(driver, keywords, 10, 0.5) == 1:
                return 1
        except:
            pass
        time.sleep(size)
        i += size
    return 没找到

# 等待样式元素css[0]
def waitcss(driver, css, long, size):
    i = 0
    while i <= long:
        page = driver.page_source
        selector = parsel.Selector(text=page)
        try:
            print(selector.css(f'{css[0]}{css[2]}').get(), css[1], selector.css(f'{css[0]}{css[2]}').get() in css[1])
            if selector.css(f'{css[0]}{css[2]}').get() in css[1]:
                return 1
        except:
            pass
        time.sleep(size)
        i += size
    return 0

# 重复任务
# taps
# 'css' : 样式等待
# 'words' : 单词等待
# 'cv' : 样式元素内容等待
def LazyAction(driver, action, css, times, taps):
    i = 0
    while i <= times:
        menu = driver.find_element(*(By.CSS_SELECTOR, css[0]))
        if action == 'move_to_element':
            ActionChains(driver).move_to_element(menu).perform()
        elif action == 'click':
            ActionChains(driver).click(menu).perform()
        else:
            return 没有类型
        if taps == 'css':
            try:
                WebDriverWait(driver, 5, 0.1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css[1])))
                return 'ok'
            except:
                pass
        elif taps == 'words':
            try:
                wait(driver, taps, 5, 0.1)
                return 'ok'
            except:
                pass
        elif taps == 'cv':
            try:
                waitcss(driver, css[1:], 5, 0.1)
                return 'ok'
            except:
                pass
        else:
            pass
        i += 1
    return 'refresh'


def base64_to_image(base64_str):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = io.BytesIO(byte_data)
    img = Image.open(image_data)
    return img

def flow(driver):
    for i in range(300, 700):
        print(i)
        url = pmysql.get(f'select TmGsLink from taobaoinfo where id={i};', get_one=True)[0]
        name = pmysql.get(f'select title from taobaoinfo where id={i};',get_one=True)[0]
        print(url)
        if 'xid' not in url:
            continue
        driver.get(url)
        WebDriverWait(driver, 5000, 0.1).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#J_CheckCode')))
        Hitimage(driver, i)
        #getimage(driver, i)

if __name__ == '__main__':
    pmysql = MY.MysqlManager('sjyy', 'root', 'Men6862471', host='localhost', port=3306, charset='utf8',
                             use_unicode=True)
    pmysql.connect_db()
    driver = opendriver()
    url = f"https://shopsearch.taobao.com/search?q='黑茶'&ie=utf8&sort=sale-desc&isb=1"
    driver.get(url)
    WebDriverWait(driver, 5000, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '#shopsearch-pager > div > div > div > div.total')))
    time.sleep(5)
    try:
        print(flow(driver))
    except EOFError as Error:
        pmysql.close_db()
        print(Error)
    pmysql.close_db()
    # 15711314130
    # flow2(driver)
