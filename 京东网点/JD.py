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
import keepprogress as kp



def opendriver():  ####获取driver
    header = choice(config.Chrome())
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["pageLoadStrategy"] = "none"  ####get禁止阻塞
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('user-agent="%s"' % header)
    driver = uc.Chrome(executable_path="chromedriver", options=chrome_options, desired_capabilities=desired_capabilities)
    return driver

#b-map-wrapper > div:nth-child(3)
#b-map-wrapper > div:nth-child(3)
# 等待字符
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
            if wait(driver,keywords,30,0.5) == 1:
                return 1
        except:
            pass
        time.sleep(size)
        i += size
    return 没找到

# 重复任务
def lazy_action(driver,action,css,times):
    i = 0
    while i <= times:
        menu = driver.find_element(*(By.CSS_SELECTOR, css[0]))
        if action == 'move_to_element':
            ActionChains(driver).move_to_element(menu).perform()
        elif action == 'click':
            ActionChains(driver).click(menu).perform()
        else:
            return 没有类型
        try:
            WebDriverWait(driver, 5, 0.1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css[1])))
            return 'ok'
        except:
            pass
        time.sleep(0.5)
        i += 1
    return 'refresh'


def to_mysql(driver):
    page = driver.page_source
    selector = parsel.Selector(text=page)
    li = selector.css("#b-list > li")

    for i in range(1, len(li) + 1):
        dit = {}
        dit['FullName'] = selector.css(f"#b-list > li:nth-child({i}) > h4::text").get()  # 全名
        loc = selector.css(f"#area1 > div.ui-area-text-wrap > div::attr(data-name)").get()
        if loc == None:
            loc = ''
        if len(loc.split('-')) < 4:
            loc_list = ['@'] * (3 - len(loc.split('-'))) + loc.split('-') + ['@']
        elif len(loc.split('-')) == 4:
            loc_list = loc.split('-')
        else:
            loc_list = ['@'] * 4

        dit['Province'], dit['City'], dit['District'], dit['street'] = loc_list
        dit['Address'] = selector.css(f"#b-list > li:nth-child({i}) > p.address::text").get()
        dit['phone'] = selector.css(f"#b-list > li:nth-child({i}) > p.tel::text").get()
        dit['openhours'] = selector.css(f"#b-list > li:nth-child({i}) > p.time::text").get()
        dit['service'] = '-'.join(selector.css(f"#b-list > li:nth-child({i}) > div > p::text").getall())
        # addnum = 0
        # for ll in loc_list:
        #     print(ll,dit['Address'])
        #     if ll in str(dit['Address'])+'qqq':
        #         addnum += 1
        # if addnum >= 2:
        print(dit)
        pmysql.insert_large(
            "INSERT INTO JDsite" + str(tuple(dit.keys())).replace("'", "") + f"VALUES{tuple(dit.values())};")







def flow(driver):
    global num
    try:
        [k1, k2, k3, k4] = kp.get(keeppath)
    except:
        [k1, k2, k3, k4] = [1, 1, 1, 1]

    if k1 >= limit[0] and k2 >= limit[1] and k3 >= limit[2] and k4 >= limit[3]:
        return 'end'
    print('正常读取进程')
    [p1, p2, p3, p4] = [1, 1, 1, 1]
    wait(driver, '卫星', 10, 0.1)

    # 移动到地区栏
    css = [
        '#area1 > div.ui-area-text-wrap',
        "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-tab > a:nth-child(1)"
    ]
    if lazy_action(driver, 'move_to_element', css, 5) == 'refresh':
        return 'refresh'


    # 点击一层地区筛选栏
    css = [
        '#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-tab > a:nth-child(1)',
        "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(1) > ul > li"
    ]
    if lazy_action(driver, 'click', css, 5) == 'refresh':
        return 'refresh'

    page = driver.page_source
    selector = parsel.Selector(text=page)

    # 第一层循环
    pro1 = selector.css(
        "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(1) > ul > li")
    print('k1',k1,len(pro1) + 1)
    for p1 in range(k1, len(pro1) + 1):
        css = [
            '#area1 > div.ui-area-text-wrap',
            "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-tab > a:nth-child(1)"
        ]
        if lazy_action(driver, 'move_to_element', css, 5) == 'refresh':
            return 'refresh'


        # 点击一层地区筛选栏
        css = [
            '#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-tab > a:nth-child(1)',
            "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(1) > ul > li"
        ]
        if lazy_action(driver, 'click', css, 5) == 'refresh':
            return 'refresh'

        print(selector.css(
            f"#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(1) > ul > li:nth-child({p1}) > a::text").get())
        menu = driver.find_element(*(By.CSS_SELECTOR,
                                     f"#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(1) > ul > li:nth-child({p1})"))
        ActionChains(driver).click(menu).perform()

        time.sleep(0.5)
        page = driver.page_source
        selector = parsel.Selector(text=page)

        pro2 = selector.css(
            "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(2) > ul > li")

        print('k2',k2,len(pro2) + 1)
        for p2 in range(k2, len(pro2) + 1):
            # 移动到地区栏
            css = [
                '#area1 > div.ui-area-text-wrap',
                 "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-tab > a:nth-child(2)"
            ]
            if lazy_action(driver, 'move_to_element', css, 5) == 'refresh':
                return 'refresh'


            # 点击二层地区筛选栏
            css = [
                '#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-tab > a:nth-child(2)',
                "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(2) > ul > li"
            ]
            if lazy_action(driver, 'click', css, 5) == 'refresh':
                return 'refresh'



            print(selector.css(
                f"#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(2) > ul > li:nth-child({p2}) > a::text").get())
            menu = driver.find_element(*(By.CSS_SELECTOR,
                                         f"#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(2) > ul > li:nth-child({p2})"))
            ActionChains(driver).click(menu).perform()
            time.sleep(0.5)
            page = driver.page_source
            selector = parsel.Selector(text=page)
            # if words == selector.css("#area1 > div.ui-area-text-wrap > div::text").get():
            
            pro3 = selector.css(
                "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(3) > ul > li")
            # 判断残留
            pro3_2 = selector.css(
                f"#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(2) > ul > li:nth-child(1) > a::text").get()
            pro3_3 = selector.css(
                f"#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(3) > ul > li:nth-child(1) > a::text").get()

            # 开始采集
            if pro3 == [] or pro3_2 == pro3_3:
                kp.keep([p1, p2, p3, p4], keeppath)
                if num >= 1:
                    return 'refresh'
                num += 1
                # 点击搜索
                css = [
                    '#b-search-btn',
                    '#b-map-wrapper > div:nth-child(3)'
                ]
                if lazy_action(driver, 'click', css, 5) == 'refresh':
                    return 'refresh'
                to_mysql(driver)
                pro3 = []
            print('k3',k3,len(pro3) + 1)
            for p3 in range(k3, len(pro3) + 1):
                # 移动到地区栏
                css = [
                    '#area1 > div.ui-area-text-wrap',
                    "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-tab > a:nth-child(3)"
                ]
                if lazy_action(driver, 'move_to_element', css, 5) == 'refresh':
                    return 'refresh'

                # 点击二层地区筛选栏
                css = [
                    '#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-tab > a:nth-child(3)',
                    "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(3) > ul > li"
                ]
                if lazy_action(driver, 'click', css, 5) == 'refresh':
                    return 'refresh'



                print(selector.css(
                    f"#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(3) > ul > li:nth-child({p3}) > a::text").get())
                menu = driver.find_element(*(By.CSS_SELECTOR,
                                             f"#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(3) > ul > li:nth-child({p3})"))
                ActionChains(driver).click(menu).perform()
                time.sleep(0.5)
                page = driver.page_source
                selector = parsel.Selector(text=page)
                # if words == selector.css("#area1 > div.ui-area-text-wrap > div::text").get():
                pro4 = selector.css(
                    "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(4) > ul > li")

                # 判断残留
                pro4_3 = selector.css(
                    f"#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(3) > ul > li:nth-child(1) > a::text").get()
                pro4_4 = selector.css(
                    f"#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(4) > ul > li:nth-child(1) > a::text").get()
                # 开始采集
                if pro4 == [] or pro4_3 == pro4_4:
                    kp.keep([p1, p2, p3, p4], keeppath)

                    if num >= 1:
                        return 'refresh'
                    num += 1
                    # 点击搜索
                    css = [
                        '#b-search-btn',
                        '#b-map-wrapper > div:nth-child(3)'
                    ]
                    if lazy_action(driver, 'click', css, 5) == 'refresh':
                        return 'refresh'

                    to_mysql(driver)
                    pro4 = []

                print('k4',k4,len(pro4) + 1)
                for p4 in range(k4, len(pro4) + 1):
                    # 移动到地区栏
                    css = [
                        '#area1 > div.ui-area-text-wrap',
                        "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-tab > a:nth-child(4)"
                    ]
                    if lazy_action(driver, 'move_to_element', css, 5) == 'refresh':
                        return 'refresh'

                    # 点击二层地区筛选栏
                    css = [
                        '#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-tab > a:nth-child(4)',
                        "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(4) > ul > li"
                    ]
                    if lazy_action(driver, 'click', css, 5) == 'refresh':
                        return 'refresh'

                    print(selector.css(
                        f"#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(4) > ul > li:nth-child({p4}) > a::text").get())
                    menu = driver.find_element(*(By.CSS_SELECTOR,
                                                 f"#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-content > div:nth-child(4) > ul > li:nth-child({p4})"))
                    ActionChains(driver).click(menu).perform()
                    kp.keep([p1, p2, p3, p4], keeppath)
                    if num >= 1:
                        return 'refresh'
                    num += 1
                    # 点击搜索
                    css = [
                        '#b-search-btn',
                        '#b-map-wrapper > div:nth-child(3)'
                    ]
                    if lazy_action(driver, 'click', css, 5) == 'refresh':
                        return 'refresh'
                    to_mysql(driver)

                k4 = 1
                # 3层回点
                css = [
                    '#area1 > div.ui-area-text-wrap',
                    "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-tab > a:nth-child(3)"
                ]
                if lazy_action(driver, 'move_to_element', css, 5) == 'refresh':
                    return 'refresh'

                css = [
                    '#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-tab > a:nth-child(3)',
                    '#b-search-btn'
                ]
                if lazy_action(driver, 'click', css, 5) == 'refresh':
                    return 'refresh'


                page = driver.page_source
                selector = parsel.Selector(text=page)
            k3 = 1

            # 2层回点
            css = [
                '#area1 > div.ui-area-text-wrap',
                "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-tab > a:nth-child(2)"
            ]
            if lazy_action(driver, 'move_to_element', css, 5) == 'refresh':
                return 'refresh'

            css = [
                '#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-tab > a:nth-child(2)',
                '#b-search-btn'
            ]
            if lazy_action(driver, 'click', css, 5) == 'refresh':
                return 'refresh'

            page = driver.page_source
            selector = parsel.Selector(text=page)

        k2 = 1
        # 1层回点
        css = [
            '#area1 > div.ui-area-text-wrap',
            "#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-tab > a:nth-child(1)"
        ]
        if lazy_action(driver, 'move_to_element', css, 5) == 'refresh':
            return 'refresh'

        css = [
            '#area1 > div.ui-area-content-wrap.ui-area-w-max > div.ui-area-tab > a:nth-child(1)',
            '#b-search-btn'
        ]
        if lazy_action(driver, 'click', css, 5) == 'refresh':
            return 'refresh'


        page = driver.page_source
        selector = parsel.Selector(text=page)
    print('flow_end')
    return "end"

if __name__ == '__main__':

    words = None
    keeppath = 'keep.csv'
    keeplimitpath = 'keeplimit.csv'
    url = "https://www.jdl.com/unroute/map"
    limit = kp.get(keeplimitpath)
    pmysql = MY.MysqlManager('sjyy', 'root', 'Men6862471', host='localhost', port=3306, charset='utf8',use_unicode=True)
    pmysql.connect_db()
    driver = opendriver()
    driver.get(url)
    wait(driver, '北京', 10, 0.1)
    num = 0



    # try:
    #     while True:
    #         print('1')
    #         fw = flow(driver)
    #         if fw == 'refresh':
    #             print('开始刷新')
    #             driver.refresh()
    #             print('2')
    #             wait(driver, '卫星', 10, 0.1)
    #             num = 0
    #         elif fw == 'end':
    #             break
    #         else:
    #             pass
    # except Exception as error:
    #     print(error)
    # finally:
    #     pmysql.close_db()
    try:
        while True:
            fw = flow(driver)
            print('flow执行正常',fw)
            if fw == 'refresh':
                print('开始刷新')
                waitrefresh(driver,'北京',10,1)
                num = 0
            elif fw == 'end':
                print('正常结束')
                break
            else:
                pass
    except Exception as error:
        print(error)
    finally:
        pmysql.close_db()
