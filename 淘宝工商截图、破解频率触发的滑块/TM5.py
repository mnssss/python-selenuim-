# -*- coding: utf-8 -*-
# Author: mn
# Date: 2023-02-05 10:19:12
# LastEditTime: 2023-02-05 10:19:12
# LastEditors: mn
# FilePath: /nfswork/code/MysqlManager.py

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
import cv2 as cv
import CV
import easyocr
from PIL import Image
# 不可改变顺序
DIC = {
    "亿":'*100000000',
    "千万":'*10000000',
    "万":'*10000',
    "千":'*1000',
    "百":'*100',
}

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
                WebDriverWait(driver, 5000, 0.1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css[1])))
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


#J_ShopSearchResult > div > div.crumb.J_TCrumb > div > div > div > ul > li.crumbSearch > form > label > input
#J_ShopSearchResult > div > div.crumb.J_TCrumb > div > div > div > ul > li.crumbSearch > form > label > input
#J_ShopSearchResult > div > div.crumb.J_TCrumb > div > div > div > ul > li.crumbSearch > form > label > input


def get_text(reader,data):
    allowlist = 'ABCDEFGHIJKLMNOPQRSTUVWXYZqwertyuiopasdfghjklzxcvbnm0123456789'  # 限制数字
    result = reader.readtext(data,allowlist=allowlist) #,allowlist ='0123456789'限制数字
    result.sort(key=lambda x: x[-1], reverse=True)
    return result



def flow():
    for i in range(1, pmysql.get("SELECT MAX(id) FROM taobaoinfo;")[0][0]+1):
        im = cv.imread(f'img/100{i}.png',cv.IMREAD_GRAYSCALE)
        print(get_text(reader_ennum,im))
        sdadsa




if __name__ == '__main__':
    pmysql = MY.MysqlManager('sjyy', 'root', 'Men6862471', host='localhost', port=3306, charset='utf8',
                             use_unicode=True)
    reader_ennum = easyocr.Reader(['ch_sim', 'en'], gpu=True)
    print(flow())

    # 15711314130
    # flow2(driver)
