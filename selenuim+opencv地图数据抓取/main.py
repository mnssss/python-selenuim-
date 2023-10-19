import parsel
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities###get阻塞
import easyocr
import pandas as pd
from PIL import Image
import config
import RGB
from random import choice, random
import csv
import keepprogress as kp
import time
import sys
sys.setrecursionlimit(100000) #例如这里设置为十万
def opendriver():####获取driver
    header = choice(config.UserHeader)
    #desired_capabilities["pageLoadStrategy"] = "none"  ####get禁止阻塞
    firefox_options = Options()
    firefox_options.add_argument('user-agent="%s"'% header)
    #firefox_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    #firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path="geckodriver", options=firefox_options)
    driver.maximize_window()
    return driver

def wait(driver,keywords,long,size):
    i = 0
    while i <= long:
        page = driver.page_source
        if page.find(keywords) != -1:
            return 1
        time.sleep(size)
        i += size
    return 0
# 截图        0不需要裁减
def ps(driver,top_x,top_y,end_x,end_y,css,path):
    im = WebDriverWait(driver, 5, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR,css)))
    im.screenshot(path)
    if top_x + top_y + end_x + end_y != 0:
        img = Image.open(path)
        img = img.crop((top_x,top_y,end_x,end_y))## 0,0表示要裁剪的位置的左上角坐标，50,50表示右下角。
        img.save(path) ## 将裁剪下来的图片保存到 举例.png

# 坐标变换
def Lat(lat):
    if lat.split('°')[1] == 'N':
        lat = -1 * eval(lat.split('°')[0])
    else:
        lat = eval(lat.split('°')[0])
    return lat

# 读取中点坐标
def located(driver):
    # 点击图片中心
    menu = driver.find_element(*(By.CSS_SELECTOR, '.cesium-widget > canvas:nth-child(1)'))
    ActionChains(driver).move_to_element_with_offset(menu,0,0).click().perform()
    wait(driver,'tjs-feature-info-panel__location',10000,1)
    # 读取中点坐标
    page = driver.page_source
    selector = parsel.Selector(text=page)
    ll = selector.css('.tjs-feature-info-panel__location > span:nth-child(2)::text').get().split(", ")
    ActionChains(driver).release().perform()
    return ll



# 按坐标定位dy=ty - fy ,1496,968
def position(driver, Ty, Tx, old_dy, old_dx, size_y, size_x):
    n = 0
    ty = Lat(Ty)
    ll = located(driver)
    fy = Lat(ll[0])
    dy = ty - fy
    tx = eval(Tx.split('°')[0])
    ttx = Tx.split('°')[1]
    fx = eval(ll[1].split('°')[0])
    ffx = ll[1].split('°')[1]

    if (ffx == 'W') and (ttx == 'W'):
        dx = tx - fx
    elif (ffx == 'E') and (ttx == 'E'):
        dx = fx - tx
    elif (ffx == 'E') and (ttx == 'W'):
        dx = abs(180-fx-tx)/(180-fx-tx) * (180-abs(180-fx-tx))
    elif (ffx == 'W') and (ttx == 'E'):
        dx = abs(tx-(180-fx)) / (tx-(180-fx)) * (180-abs(tx-(180-fx)))
    else:
        dx = 0
        print(ffx,ttx)
        print('坐标错误')
    if old_dx == 'a':
        old_dx = 2*dx
    if (abs(dx) >  0.001) and (abs(dx - old_dx) > 0.0001):
        if dx * old_dx < 0:
            size_x /= 2
        if dx > 0:
            menu = driver.find_element(*(By.CSS_SELECTOR, '.cesium-widget > canvas:nth-child(1)'))
            ActionChains(driver).move_to_element_with_offset(menu, -738, 400).click_and_hold().perform()
            tar = -738+size_x
            ActionChains(driver, duration=250).move_to_element_with_offset(menu, tar, 400).perform()
            ActionChains(driver).pause(0.5).release().perform()
            if size_x < 5:
                wait(driver, 'background-color: rgb(255, 255, 255); width: 100%', 10000, 1)
        else:
            menu = driver.find_element(*(By.CSS_SELECTOR, '.cesium-widget > canvas:nth-child(1)'))
            ActionChains(driver).move_to_element_with_offset(menu, 738, 400).click_and_hold().perform()
            tar = 738-size_x
            ActionChains(driver, duration=250).move_to_element_with_offset(menu, tar, 400).perform()
            ActionChains(driver).pause(0.5).release().perform()
            if size_x < 5:
                wait(driver, 'background-color: rgb(255, 255, 255); width: 100%', 10000, 1)
        n = 1
    else:
        pass



    if old_dy == 'a':
        old_dy = 2*dy
    # 纬度校准
    if (abs(dy) >  0.001) and (abs(dy - old_dy) > 0.0001):
        if dy * old_dy < 0:
            size_y /= 2
        if dy > 0:
            menu = driver.find_element(*(By.CSS_SELECTOR, '.cesium-widget > canvas:nth-child(1)'))
            ActionChains(driver).move_to_element_with_offset(menu, 0, 449).click_and_hold().perform()
            tar = 449-size_y
            ActionChains(driver, duration=250).move_to_element_with_offset(menu, 0, tar).perform()
            ActionChains(driver).pause(0.5).release().perform()
            if size_y < 5:
                wait(driver, 'background-color: rgb(255, 255, 255); width: 100%', 10000, 1)
        else:
            menu = driver.find_element(*(By.CSS_SELECTOR, '.cesium-widget > canvas:nth-child(1)'))
            ActionChains(driver).move_to_element_with_offset(menu, 0, -449).click_and_hold().perform()
            tar = -449+size_y
            ActionChains(driver, duration=250).move_to_element_with_offset(menu, 0, tar).perform()
            ActionChains(driver).pause(0.5).release().perform()
            if size_y < 5:
                wait(driver, 'background-color: rgb(255, 255, 255); width: 100%', 10000, 1)
        n = 1
    else:
        pass


    if n == 1:
        position(driver, Ty,Tx , dy, dx, size_y, size_x)

#                 N     E
def drift(driver,star_y,star_x,end_y,end_x,ll,num):

    if eval(star_x.split('°')[0]) < eval(ll[1].split('°')[0]) and num % 2 == 1:
        menu = driver.find_element(*(By.CSS_SELECTOR, '.cesium-widget > canvas:nth-child(1)'))
        ActionChains(driver).move_to_element_with_offset(menu,-593, 400).click_and_hold().perform()
        ActionChains(driver, duration=250).move_to_element_with_offset(menu, 593, 400).perform()
        ActionChains(driver).pause(0.5).release().perform()
        wait(driver, 'background-color: rgb(255, 255, 255); width: 100%', 10000, 1)
        return 1, num
    elif eval(ll[1].split('°')[0]) < eval(end_x.split('°')[0]) and num % 2 == 0:
        menu = driver.find_element(*(By.CSS_SELECTOR, '.cesium-widget > canvas:nth-child(1)'))
        ActionChains(driver).move_to_element_with_offset(menu, 593, 400).click_and_hold().perform()
        ActionChains(driver, duration=250).move_to_element_with_offset(menu, -593, 400).perform()
        ActionChains(driver).pause(0.5).release().perform()
        wait(driver, 'background-color: rgb(255, 255, 255); width: 100%', 10000, 1)
        return 1, num
    else:
        pass


    if eval(ll[0].split('°')[0]) < eval(end_y.split('°')[0]):
        num += 1
        menu = driver.find_element(*(By.CSS_SELECTOR, '.cesium-widget > canvas:nth-child(1)'))
        ActionChains(driver).move_to_element_with_offset(menu, 0, -409).click_and_hold().perform()
        ActionChains(driver, duration=250).move_to_element_with_offset(menu, 0, 409).perform()
        ActionChains(driver).pause(0.5).release().perform()
        wait(driver, 'background-color: rgb(255, 255, 255); width: 100%', 10000, 1)
        return 1,num

    return 0,num



url = 'https://www.nationalmap.gov.au/#share=s-py9ofDCNEwqsrfGGkptS5dJ9wSq'
# url = 'https://wsgs.sbj.cnipa.gov.cn:9080/tmpu/pingshen/getMain.html'
keeppath = 'kp/map.csv'
# f = open('DownloadLink/wwwdianpingcom.csv', mode='a', encoding='utf-8', newline='')
# # 表头信息
# csv_writer = csv.DictWriter(f, fieldnames=['店名', 'in'])
# # 写入表头
# csv_writer.writeheader()
# sudo pip3 install --index-url https                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                pypi.douban.com/simple parsel 加快
# pip3 install -i https://pypi.douban.com/simple parsel  windows

driver = opendriver()
driver.get(url)
wait(driver,'WelcomeMessage___StyledRawButton-sc-1xu3b82-1',1000,0.5)
menu = driver.find_element(*(By.CSS_SELECTOR, '.WelcomeMessage___StyledRawButton-sc-1xu3b82-1'))
ActionChains(driver).click(menu).perform()
if wait(driver,'Got it, thanks!',10,0.5):
    menu = driver.find_element(*(By.CSS_SELECTOR, 'div.jCpKfi:nth-child(4) > button:nth-child(1)'))
    ActionChains(driver).click(menu).perform()

wait(driver,'tjs-menu-bar__flex',1000,0.5)
# 点击设置
menu = driver.find_element(*(By.CSS_SELECTOR, '.tjs-menu-bar__flex > ul:nth-child(1) > li:nth-child(1) > div:nth-child(1) > button:nth-child(1) > span:nth-child(2)'))
ActionChains(driver).click(menu).perform()
time.sleep(5)

wait(driver,'Button__RawButton-sc-1hi1t24-3',1000,0.5)
# 点击地图样式
menu = driver.find_element(*(By.CSS_SELECTOR, 'button.Button__RawButton-sc-1hi1t24-3:nth-child(7) > img:nth-child(1)'))
ActionChains(driver).click(menu).perform()
wait(driver,'InnerPanel___StyledButton-sc-1bhp2fc-1',1000,0.5)
# 关闭设置窗口
menu = driver.find_element(*(By.CSS_SELECTOR, '.InnerPanel___StyledButton-sc-1bhp2fc-1'))
ActionChains(driver).click(menu).perform()
# 等待进度条
wait(driver,'background-color: rgb(255, 255, 255); width: 100%',10000,1)


# 点击放大按钮
wait(driver,'Box-sc-lks5ro-0',10000,1)
menu = driver.find_element(*(By.CSS_SELECTOR, 'ul.Box-sc-lks5ro-0:nth-child(1) > li:nth-child(1) > button:nth-child(1) > svg:nth-child(1)'))
ActionChains(driver).click(menu).perform()
time.sleep(1)
ActionChains(driver).click(menu).perform()
time.sleep(1)
ActionChains(driver).click(menu).perform()
time.sleep(1)
ActionChains(driver).click(menu).perform()
wait(driver,'background-color: rgb(255, 255, 255); width: 100%',10000,1)

# 写入数据
f = open('nationalmap.csv', mode='a', encoding='utf-8-sig', newline='')
# 表头信息
csv_writer = csv.DictWriter(f, fieldnames=['坐标', 'Pumped hydro', '代号', 'Class', 'Head (m)', 'Separation (km)', 'Average Slope (%)',
                                           'Volume (GL)', 'Water to Rock (Pair)', 'Energy (GWh)',
                                           'Storage time (h)'])
# 写入表头
csv_writer.writeheader()






try:
    tar = kp.get('中国坐标保存进度.csv')
except:
    kp.keep(['3°N|73°E',0],'中国坐标保存进度.csv')
    tar = kp.get('中国坐标保存进度.csv')
position(driver, tar[0].split('|')[0], tar[0].split('|')[1], 'a', 'a', 898, 1476)
wait(driver, 'background-color: rgb(255, 255, 255); width: 100%', 10000, 1)
print('初始定位结束')
while True:
    ll = located(driver)
    # 点击关闭信息兰
    menu = driver.find_element(*(By.CSS_SELECTOR, '.tjs-feature-info-panel__btn--close-feature'))
    ActionChains(driver).click(menu).perform()
    ActionChains(driver).release().perform()
    kp.keep([ll[0]+'|'+ll[1], tar[1]], '中国坐标保存进度.csv')
    print(ll, '正在进行')
    print('开始截图')
    # 地图截图
    #ps(driver,105,50,1391,918,'.cesium-widget > canvas:nth-child(1)','地图.png')
    ps(driver, 105, 75, 1391, 893, '.cesium-widget > canvas:nth-child(1)', '地图.png')
    print('截图完毕')
    # 读取坐标
    rgb = RGB.RGB('地图.png')
    print(rgb.coord_r)
    # 转换点击
    for j in rgb.coord_r:
        sx = j[1]-643+1
        sy = j[0]-409+3.5
        wait(driver, 'background-color: rgb(255, 255, 255); width: 100%', 10000, 1)
        # 点击目标点
        sxx=0
        syy=0
        w = 0
        while w <= 5:
            w += 1
            menu = driver.find_element(*(By.CSS_SELECTOR, '.cesium-widget > canvas:nth-child(1)'))
            ActionChains(driver).move_to_element_with_offset(menu, sx+sxx, sy+syy).click().perform()
            wait(driver, 'background-color: rgb(255, 255, 255); width: 100%', 10000, 1)
            ActionChains(driver).release().perform()

            if wait(driver, 'Average Slope (%)', 1.5, 0.5):
                dit = {}
                page = driver.page_source
                selector = parsel.Selector(text=page)
                dit['坐标'] = selector.css('.tjs-feature-info-panel__location > span:nth-child(2)::text').get()
                dit['Pumped hydro'] = selector.css('li.tjs-feature-info-section__section:nth-child(1) > button:nth-child(1) > span:nth-child(1)::text').get()
                dit['代号'] = selector.css('.tjs-feature-info-section__content > div:nth-child(2) > span:nth-child(1) > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1)::text').get()
                dit['Class'] = selector.css('.tjs-feature-info-section__content > div:nth-child(2) > span:nth-child(1) > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)::text').get()
                dit['Head (m)'] = selector.css('.tjs-feature-info-section__content > div:nth-child(2) > span:nth-child(1) > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)::text').get()
                dit['Separation (km)'] = selector.css('.tjs-feature-info-section__content > div:nth-child(2) > span:nth-child(1) > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2)::text').get()
                dit['Average Slope (%)'] = selector.css('.tjs-feature-info-section__content > div:nth-child(2) > span:nth-child(1) > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2)::text').get()
                dit['Volume (GL)'] = selector.css('.tjs-feature-info-section__content > div:nth-child(2) > span:nth-child(1) > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2)::text').get()
                dit['Water to Rock (Pair)'] = selector.css('.tjs-feature-info-section__content > div:nth-child(2) > span:nth-child(1) > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(2)::text').get()
                dit['Energy (GWh)'] = selector.css('.tjs-feature-info-section__content > div:nth-child(2) > span:nth-child(1) > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(2)::text').get()
                dit['Storage time (h)'] = selector.css('.tjs-feature-info-section__content > div:nth-child(2) > span:nth-child(1) > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(8) > td:nth-child(2)::text').get()
                if (dit['Class'] is not None):
                    csv_writer.writerow(dit)  # 写到for循环内
                    f.flush()
                # 点击关闭信息兰
                menu = driver.find_element(*(By.CSS_SELECTOR, '.tjs-feature-info-panel__btn--close-feature'))
                ActionChains(driver).click(menu).perform()
                ActionChains(driver).release().perform()
                wait(driver, 'background-color: rgb(255, 255, 255); width: 100%', 10000, 1)
                break


            sxx = 3*(random()-0.5)
            syy = 3 * (random() - 0.5)
            # 点击关闭信息兰
            menu = driver.find_element(*(By.CSS_SELECTOR, '.tjs-feature-info-panel__btn--close-feature'))
            ActionChains(driver).click(menu).perform()
            ActionChains(driver).release().perform()
            wait(driver, 'background-color: rgb(255, 255, 255); width: 100%', 10000, 1)

    #定位
    print('开始位移')
    dr = drift(driver,'3°N','73°E','19°N','136°E',ll,tar[1])
    if dr[0] == 0:
        break
    tar[1] = dr[1]
    print('位移结束')


# # 获取中点坐标
# ll = located(driver)

#position(driver, '25°S', '138°E', 'a', 'a',898,1476)

print('完成')






