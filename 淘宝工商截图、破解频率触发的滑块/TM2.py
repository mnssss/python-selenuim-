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
    if wait(driver,css[5],0.5,0.1):
        pass
    else:
        return 0
    # 判断是否是滑块正常状态
    # 15711314130
    if waitcss(driver,css,0.1,0.1):
        print('开始滑动')
        # menu = driver.find_element(*(By.CSS_SELECTOR, css[3]))
        # ActionChains(driver).click_and_hold(menu).perform()
        # js = f"let btn = document.querySelector({css[3]});" \
        #      "let step = 1;" \
        #      "btn.addEventListener('onmouseover',function(){" \
        #      "let timer = setInterval(function(){" \
        #      "let o_left = parseInt(btn.style.left);" \
        #      "let n_left = o_left+step;" \
        #      "btn.style.left = n_left+'px';" \
        #      "if ( n_left>200) {" \
        #      "clearInterval(timer);" \
        #      "};},10);});" \
        #      "let ev = new Event('onmouseover');" \
        #      "btn.dispatchEvent(ev);"
        # driver.execute_script(js)
        menu = driver.find_element(*(By.CSS_SELECTOR, css[3]))
        ActionChains(driver).click_and_hold(menu).perform()
        time.sleep(0.5)
        ActionChains(driver).move_to_element_with_offset(menu, 300, 100*random()-50).perform()
        # for i in site_to_site(star, end):
        #     ActionChains(driver).move_to_element_with_offset(menu, i[0], i[1]).perform()
        ActionChains(driver).pause(1).release().perform()
        try:
            WebDriverWait(driver, 0.5, 0.1).until(
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


def flow(driver):
    for i in range(1, pmysql.get("SELECT MAX(id) FROM taobaoinfo;")[0][0]+1):
        print(i)
        url = pmysql.get(f'select userRateUrl from taobaoinfo where id={i};', get_one=True)[0]
        # if '?xid=' in pmysql.get(f'select TmGsLink from taobaoinfo where id={i};', get_one=True)[0]:
        #     continue
        print(url)
        driver.get(url)
        # nc_1_n1z
        css = [
            '#nc_1__scale_text > span',  # 滑块区域
            '请按住滑块，拖动到最右边',  # 滑块文字
            '::text',  # 滑块模块
            '#nc_1_n1z',  # 滑块
            '#\`nc_1_refresh1\`',  # 滑块出错
            '亲，请拖动下方滑块完成验证'
        ]
        slide(driver, css, [-130,1], [130,200])

        WebDriverWait(driver, 5000, 1).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              '#shop-rate-box > div.personal-info.personal-info-fullwidth.layout.grid-s6m0 > div.col-sub > div:nth-child(1) > div.hd')))

        page = driver.page_source
        selector = parsel.Selector(text=page)
        dit = {}
        # dit['ind'] = str(selector.css(
        #     "#shop-rate-box > div.personal-info.personal-info-fullwidth.layout.grid-s6m0 > div.col-sub > div:nth-child(1) > div.bd > div > ul > li:nth-child(1) > a::text").get())
        # dit['mas'] = str(selector.css(
        #     "#dsr > li:nth-child(1) > div.item-scrib > em.count::attr(title)").get())
        # dit['mg'] = str(selector.css(
        #     "#dsr > li:nth-child(1) > div.item-scrib > em:nth-child(3) > strong::attr(class)").get()) + "|" + \
        #             str(selector.css(
        #                 "#dsr > li:nth-child(1) > div.item-scrib > em:nth-child(3) > strong::text").get())
        # dit['sas'] = str(selector.css(
        #     "#dsr > li:nth-child(2) > div.item-scrib > em.count::attr(title)").get())
        # dit['sg'] = str(selector.css(
        #     "#dsr > li:nth-child(2) > div.item-scrib > em:nth-child(3) > strong::attr(class)").get()) + "|" + \
        #             str(selector.css(
        #                 "#dsr > li:nth-child(2) > div.item-scrib > em:nth-child(3) > strong::text").get())
        # dit['cas'] = str(selector.css(
        #     "#dsr > li:nth-child(3) > div.item-scrib > em.count::attr(title)").get())
        # dit['cg'] = str(selector.css(
        #     "#dsr > li:nth-child(3) > div.item-scrib > em:nth-child(3) > strong::attr(class)").get()) + "|" + \
        #             str(selector.css(
        #                 "#dsr > li:nth-child(3) > div.item-scrib > em:nth-child(3) > strong::text").get())
        # dit['TmGsLink'] = "https:" + str(selector.css(
        #     "#J_ShowLicence::attr(href)").get())
        dit['encodeNick'] = "https:" + str(selector.css(
            "#shopExtra > div.slogo > a::attr(href)").get())

        dit['shopCount'] = str(selector.css("#dsr > li.J_RateInfoTrigger.dsr-item.selected > div.dsr-info-box > div > div.total > span:nth-child(3)::text").get())

        # # 点击
        # css=[
        #     "#J_ShowLicence > img",
        #
        # ]
        # if LazyAction(driver, 'click', css, 5, 'css') == 'refresh':
        #     return 'refresh'

        print(dit)
        Keys = []
        for d in dit.keys():
            Keys.append(f"{d}='{dit[d]}'")
        pmysql.update(f"UPDATE taobaoinfo SET {','.join(Keys)} WHERE id={i};")


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
