import csv
import datetime
import os

from selenium import webdriver
# 抓取主页数据
from selenium.webdriver import DesiredCapabilities
from pyquery import PyQuery as pq
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


dcap = dict(DesiredCapabilities.PHANTOMJS)
#从USER_AGENTS选一个浏览器头，伪装浏览器
dcap["phantomjs.page.settings.userAgent"] = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1')
# 不载入图片，爬页面速度会快很多
dcap["phantomjs.page.settings.loadImages"] = False
# 设置代理
# service_args = ['--proxy=127.0.0.1:9999','--proxy-type=socks5']
service_args = [
    '--proxy=%s' % "218.60.8.83:3129",    # 代理 IP：prot    （eg：192.168.0.28:808）
    '--proxy-type=http',         # 代理类型：http/https/socks5
    '--load-images=no',           # 关闭图片加载（可选）
    '--disk-cache=yes',            # 开启缓存（可选）
    '--ignore-ssl-errors=true'  # 忽略https错误（可选）
]

#打开带配置信息的phantomJS浏览器
# browser = webdriver.PhantomJS(executable_path="C:/Python/Scripts/phantomjs.exe", desired_capabilities=dcap, service_args=service_args)
# # 隐式等待5秒，可以自己调节
# browser.implicitly_wait(5)
# # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
# # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
# browser.set_page_load_timeout(10)
# # 设置10秒脚本超时时间
# browser.set_script_timeout(10)


browser = webdriver.PhantomJS(desired_capabilities=dcap)
wait = WebDriverWait(browser, 5)
url = 'https://m.ctrip.com/webapp/hotel/hoteldetail/1451725.html?atime=20190718&daylater=0&days=1&contrl=0&pay=0&discount=&latlon=&listindex=4&userLocationSearch=false#fromList'
# url = 'https://m.ctrip.com/webapp/hotel/oversea/hoteldetail/532149.html?atime=20190718'
try:
    browser.get(url)
    html = browser.page_source
    # print(html)

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#content > div > ul > li.item.recommend-item.dl-price-layout.js_baseroom_item > div.cell-star.room-column.room--space > div')))
        print('加载成功')
    except:
        print("获取表格元素失败")
    #每一个房型下的所有价格
    allrooms = browser.find_elements_by_xpath('//*[@class="sub-romm js_childroomlist"]')
    roomIDs = browser.find_elements_by_xpath('//*[@class="cell-star room-bd js_show_baseroom"]')
    # 每个房型只有一个名字
    roomtypes = browser.find_elements_by_xpath('//*[@class="cell-star room-column room--space"]//h3')
    roomdescs = browser.find_elements_by_xpath('//*[@class="cell-star room-column room--space"]//p[@class="room-size"]')
    roompolicies = browser.find_elements_by_xpath('//*[@class="cell-star room-column room--space"]//div[@class="left-shrink"]')
    prices = browser.find_elements_by_xpath('//*[@class="cell-star dl-price-align js_base_new_price_area"]//span[@class="price"]')
    print(len(allrooms),len(roomIDs),len(roomtypes),len(roomdescs),len(prices),len(roompolicies))
    # 写入EXCEL
    if os.path.exists("room.csv"):
        os.remove('room.csv')
    with open('room.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['UnitTypeID','UnitTypeName','BedType','Price','Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    if prices:
        for i in range(0,len(roomtypes)):
            if(i < len(roomIDs)):
                roomid = str(roomIDs[i].get_attribute('data-bid'))
            if(i < len(roomtypes)):
                roomtype = str(roomtypes[i].text)[:-4]
            price = str(prices[i].text)[1:-1]
            policy = str(roompolicies[i].text)
            roomdesc = str(roomdescs[i].text).split()
            # area = roomdescs[0]
            bed = roomdesc[1]
            window = roomdesc[2]
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            room = {
                'UnitTypeID': roomid,
                'UnitTypeName': roomtype,
                'BedType': bed,
                'Price': price,
                'Date': date
            }
            # print(roomtypes[i].text,prices[i].text,roomdescs[i].text)
            print(roomid,roomtype,bed,price,window,date)
            try:
                with open('room.csv', 'a', encoding='utf-8', newline='') as csvfile:
                    fieldnames = ['UnitTypeID','UnitTypeName','BedType','Price','Date']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow(room)
            except:
                print('写入CSV失败')
finally:
    browser.quit()