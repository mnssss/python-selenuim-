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

def opendriver():  ####获取driver
    header = choice(config.Chrome())
    # desired_capabilities = DesiredCapabilities.CHROME
    # desired_capabilities["pageLoadStrategy"] = "none"  ####get禁止阻塞
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('user-agent="%s"' % header)
    driver = uc.Chrome(executable_path="chromedriver", options=chrome_options)
    return driver

# 强制等待字符
def wait(driver, keywords, long, size):
    i = 0
    while i <= long:
        page = driver.page_source
        if page.find(keywords) != -1:
            return 1
        time.sleep(size)
        i += size
    return 没找到

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

# 等待样式元素
def waitcss(driver, css, long, size):
    i = 0
    while i <= long:
        page = driver.page_source
        selector = parsel.Selector(text=page)
        print(selector.css(f'{css[0]}{css[2]}').get(), css[1], selector.css(f'{css[0]}{css[2]}').get() in css[1])
        if selector.css(f'{css[0]}{css[2]}').get() in css[1]:
            return 1
        time.sleep(size)
        i += size
    return 没找到

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

def to_mysql(driver):
    # range-query-citypicker > div > div.tabs > ul > li:nth-child(3)
    page = driver.page_source
    selector = parsel.Selector(text=page)
    # 循环获取列表
    pro1 = selector.css("#list-container > li")
    for p1 in range(1,len(pro1) + 1):
        page = driver.page_source
        selector = parsel.Selector(text=page)
        dit = {}
        if selector.css(f'#list-container > li:nth-child({p1}) > div') == []:
            div = '>'
        else:
            div = '> div >'
        # 移动到小标志
        css = [
            f'#list-container > li:nth-child({p1}) {div} ul > li.list-info.icon-5zhe > div > div > div.descr-icon',
            f"#list-container > li:nth-child({p1}) {div} ul > li.list-info.icon-5zhe > h4 > a.shop-name.J_shop_name"
        ]
        if LazyAction(driver, 'move_to_element', css, 5, 'css') == 'refresh':
            return 'refresh'
        dit['title'] = str(selector.css(
            f"#list-container > li:nth-child({p1}) {div} ul > li.list-info.icon-5zhe > h4 > a.shop-name.J_shop_name::text").get()).replace(
            ' ', '').replace('\n', '')
        dit['ranks'] = str(p1)
        dit['pageNum'] = str(selector.css(f"#J_relative > div.sort-row > div > div > div.pager > ul > li:nth-child(2) > span::text").get())
        dit['userRateUrl'] = 'https:' + str(selector.css(
            f"#list-container > li:nth-child({p1}) {div} ul > li.list-info.icon-5zhe > h4 > a.icon-service-tianmao-large::attr(href)").get())
        dit['shopUrl'] = 'https:' + str(selector.css(
            f"#list-container > li:nth-child({p1}) {div} ul > li.list-info.icon-5zhe > h4 > a.shop-name.J_shop_name::attr(href)").get())
        dit['provcity'] = str(selector.css(
            f"#list-container > li:nth-child({p1}) {div} ul > li.list-info.icon-5zhe > p.shop-info > span.shop-address::text").get())
        dit['queryWord'] = i
        dit['uid'] = str(selector.css(
            f"#list-container > li:nth-child({p1}) {div} ul > li.list-info.icon-5zhe > h4 > a.icon-service-tianmao-large::attr(trace-uid)").get())

        # dit['spm'] = str(selector.css(
        #     f"#list-container > li:nth-child({p1}) {div} ul > li.list-info.icon-5zhe > h4 > a.icon-service-tianmao-large::attr(data-spm-anchor-id)").get())

        print(dit)
        pmysql.insert_large(
            "INSERT INTO taobaoinfo" + str(tuple(dit.keys())).replace("'", "") + f"VALUES{tuple(dit.values())};")


def flow(driver):
    while True:
        to_mysql(driver)
        # 点击下一页
        css = [
            '#shopsearch-pager > div > div > div > ul > li.item.next > a',
            '#shopsearch-pager > div > div > div > div.total'
        ]
        try:
            if LazyAction(driver, 'click', css, 5, 'css') == 'refresh':
                return 'refresh'
            time.sleep(2)
        except:
            break
        try:
            WebDriverWait(driver, 10, 1).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#shopsearch-pager > div > div > div > ul > li.item.next')))
        except:
            return 'end'


def flow2(driver):
    for i in range(1, pmysql.get()):
        print(i)
        url = pmysql.get(f'select shopUrl from taobaoinfo where id={i};', get_one=True)[0]
        print(url)
        driver.get(url)
        time.sleep(1)
        css = [
            '#shopExtra > div.slogo > a > strong',
            "div[id^='ks-component'] > div > div > div > div.shop-rate > ul > li:nth-child(1) > a > em"
        ]
        if LazyAction(driver, 'move_to_element', css, 5, 'css') == 'refresh':
            return 'refresh'
        page = driver.page_source
        selector = parsel.Selector(text=page)
        dit = {}
        dit['mas'] = str(selector.css(
            "div[id^='ks-component'] > div > div > div > div.shop-rate > ul > li:nth-child(1) > a > em::attr(title)").get())
        dit['mg'] = str(selector.css(
            "div[id^='ks-component'] > div > div > div > div.shop-rate > ul > li:nth-child(1) > a > span > i::text").get()) + "|" + \
                    str(selector.css(
                        "div[id^='ks-component'] > div > div > div > div.shop-rate > ul > li:nth-child(1) > a > span > em::text").get())

        dit['sas'] = str(selector.css(
            "div[id^='ks-component'] > div > div > div > div.shop-rate > ul > li:nth-child(2) > a > em::attr(title)").get())

        dit['sg'] = str(selector.css(
            "div[id^='ks-component'] > div > div > div > div.shop-rate > ul > li:nth-child(2) > a > span > i::text").get()) + "|" + \
                    str(selector.css(
                        "div[id^='ks-component'] > div > div > div > div.shop-rate > ul > li:nth-child(2) > a > span > em::text").get())


        dit['cas'] = str(selector.css(
            "div[id^='ks-component'] > div > div > div > div.shop-rate > ul > li:nth-child(3) > a > em::attr(title)").get())
        dit['cg'] = str(selector.css(
            "div[id^='ks-component'] > div > div > div > div.shop-rate > ul > li:nth-child(3) > a > span > i::text").get()) + "|" + \
                    str(selector.css(
                        "div[id^='ks-component'] > div > div > div > div.shop-rate > ul > li:nth-child(3) > a > span > em::text").get())

        dit['tm-gsLink'] = str(selector.css("div[id^='ks-component'] > div > div > div > div.extend > ul > li:nth-child(5) > div > a::attr(href)"))
        print(dit)
        Keys = []
        for d in dit.keys():
            Keys.append(f"{d}='{dit[d]}'")
        pmysql.update(f"UPDATE taobaoinfo SET {','.join(Keys)} WHERE id={i};")


if __name__ == '__main__':
    keeppath = 'keep.csv'
    keeplimitpath = 'keeplimit.csv'
    pmysql = MY.MysqlManager('sjyy', 'root', 'Men6862471', host='localhost', port=3306, charset='utf8',
                             use_unicode=True)
    pmysql.connect_db()
    driver = opendriver()
    # keysword = ['炒青绿茶','烘青绿茶','晒青绿茶','蒸青绿茶','眉茶','珠茶','细嫩炒青','大方','碧螺春','雨花茶','甘露','松针','普通烘青','细嫩烘青','川青','滇青','陕青','煎茶','玉露','小种红茶','工夫红茶','红碎茶',
    #             '正山小种','烟小种','川红','金甘露','红甘露','祁红','滇红','闽红','金骏眉','叶茶','碎茶','片茶','末茶',
    #             ]
    # ['绿茶','红茶','乌龙茶','白茶','黄茶','黑茶']
    keysword = ['白茶','黄茶','黑茶']
    for i in keysword:
        url = f"https://shopsearch.taobao.com/search?q={i}&ie=utf8&sort=sale-desc&isb=1&s=20"
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