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


def flow(driver):
    for i in range(691, pmysql.get("SELECT MAX(id) FROM taobaoinfo;")[0][0]+1):
        shop = pmysql.get(f"select encodeNick from taobaoinfo where id={i};", get_one=True)[0].replace("https://", "").split(".")[:2]
        url = f"https://{'.'.join(shop)}.com/search.htm?search=y&orderType=hotsell_desc&pageNo=1&tsearch=y"
        print(i)
        print(url)
        # if 'shop' not in url:
        #     continue
        driver.get(url)
        WebDriverWait(driver, 5000, 1).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#J_ShopSearchResult > div > div.J_TItems')))

        ### 输入文本
        menu = driver.find_element(*(By.CSS_SELECTOR, '#J_ShopSearchResult > div > div.crumb.J_TCrumb > div > div > div > ul > li.crumbSearch > form > label > input'))  ##找位置
        menu.clear()  # 清除文本框内容
        menu.send_keys("茶叶")  # 输入

        css = [
            f"#J_ShopSearchResult > div > div.crumb.J_TCrumb > div > div > div > ul > li.crumbSearch > form > input.crumbSearch-btn.J_TCrumbSearchBtn",
            f"#J_ShopSearchResult > div > div.J_TItems"
        ]
        if LazyAction(driver, 'click', css, 5, 'css') == 'refresh':
            return 'refresh'

        page = driver.page_source
        selector = parsel.Selector(text=page)
        page_num = int(selector.css("#J_ShopSearchResult > div > div.filter.clearfix.J_TFilter > p > b.ui-page-s-len::text").get().split('/')[1])

        sale_area = ''
        sale_num = ''

        # css = [
        #     f"#J_ShopSearchResult > div > div.filter.clearfix.J_TFilter > p > a.ui-page-s-next",
        #     f"#J_ShopSearchResult > div > div.J_TItems"
        # ]
        # if LazyAction(driver, 'click', css, 5, 'css') == 'refresh':
        #     return 'refresh'

        for j in range(1,page_num + 1):
            page = driver.page_source
            selector = parsel.Selector(text=page)
            fis = selector.css("#J_ShopSearchResult > div > div.J_TItems > div")
            for z in range(1,len(fis)+1):
                if selector.css(f"#J_ShopSearchResult > div > div.J_TItems > div:nth-child({z})::attr(class)").get()=="pagination":
                    break
                sale_area = str(selector.css("div.sale-area::text").get())
                sale_num += '@' + '@'.join(selector.css(f"div:nth-child({z}) > * > * > * > div.sale-area > span::text").getall()).replace("+","").replace("-","")

            css = [
                f"#J_ShopSearchResult > div > div.filter.clearfix.J_TFilter > p > *.ui-page-s-next",
                f"#J_ShopSearchResult > div > div.J_TItems"
            ]
            if LazyAction(driver, 'click', css, 5, 'css') == 'refresh':
                return 'refresh'

        for d in DIC.keys():
            sale_num = sale_num.replace(d, DIC[d])
        try:
            sale_num = str(eval(sale_num.replace('@','+')))
            print(sale_area + sale_num)
            pmysql.update(f"UPDATE taobaoinfo SET shopCount='{sale_area + sale_num}' WHERE id={i};")
        except:
            print('报错了',sale_num)



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
