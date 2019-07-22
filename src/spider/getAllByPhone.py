import csv
import datetime
import os
import time
from selenium import webdriver
# 抓取主页数据(爬下来的网页class名字有的有变动！！！！！！！！！)
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import base64

# 创建CSV
if os.path.exists("room.csv"):
    os.remove('room.csv')
with open('room.csv', 'w', encoding='utf-8', newline='') as csvfile:
    fieldnames = ['UnitTypeID', 'UnitTypeName','ProductName', 'Breakfast', 'BedType', 'PeopleNum', 'CancelRule',
                  'BusinessDate', 'Price', 'CreateTime']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

#抓取未来三天
for day in range(3):
    print('第', day, '天抓取：')

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    #从USER_AGENTS选一个浏览器头，伪装浏览器，下面可以更换的请求头
    # Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)
    # MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1
    dcap["phantomjs.page.settings.userAgent"] = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36')
    # 不载入图片，爬页面速度会快很多
    dcap["phantomjs.page.settings.loadImages"] = False
    # 代理设置
    # service_args = [
    #     '--proxy=http://fr.proxymesh.com:31280',
    #     '--proxy-type=http',
    # ]
    # authentication_token = "Basic " + base64.b64encode('username:password')
    # dcap['phantomjs.page.customHeaders.Proxy-Authorization'] = authentication_token

    # 设置代理
    # service_args = [
    #     '--proxy=%s' % "218.60.8.83:3129",    # 代理 IP：prot    （eg：192.168.0.28:808）
    #     '--proxy-type=http',         # 代理类型：http/https/socks5
    #     '--load-images=no',           # 关闭图片加载（可选）
    #     '--disk-cache=yes',            # 开启缓存（可选）
    #     '--ignore-ssl-errors=true'  # 忽略https错误（可选）
    # ]

    # 创建phantomjs网页驱动器
    # browser = webdriver.PhantomJS(desired_capabilities=dcap)
    browser = webdriver.PhantomJS()
    # 等待响应时间为10s
    wait = WebDriverWait(browser, 10)
    # url = 'https://m.ctrip.com/webapp/hotel/hoteldetail/1451725.html?atime=20190718&daylater=0&days=1&contrl=0&pay=0&discount=&latlon=&listindex=4&userLocationSearch=false#fromList'
    # url后缀
    date = int(datetime.datetime.now().strftime('%Y%m%d'))+day
    BusinessDate = datetime.datetime.strptime(str(date), "%Y%m%d").strftime('%Y-%m-%d')
    url = 'https://m.ctrip.com/webapp/hotel/hoteldetail/532149.html?days=1&atime='+str(date)+'&contrl=0&num=undefined&biz=undefined'
    # url = 'https://m.ctrip.com/webapp/hotel/hoteldetail/532149.html?days=1&atime=20190719&contrl=0&num=undefined&biz=undefined'
    print(url)

    #selenium开始解析网页
    try:
        browser.get(url)
        # 判断页面中有无此元素,有则页面加载成功
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#content > div > ul')))
            print('加载成功')
        except:
            print("获取表格元素失败")

        html = browser.page_source
        doc = pq(html)

        # 获取所有房型的名字
        roomtypes = doc('.cell-star.room-bd.js_show_baseroom')
        typenamelist = []
        for i in roomtypes.items():
            typename = i.find('h3')
            typename.find('span').remove()
            typenamelist.append(typename.text())
        print("共有房型数：", len(typenamelist))

        # 获取每个房型下面的详细列表
        allroomtypes = doc('.dl-room-type.js_roomlist .sub-romm.js_childroomlist')
        num = 0
        for j in allroomtypes.items():
            details = j.find('.item.sub-price-layout ')
            for k in details.items():
                roomid = str(k.attr('data-roomid'))  #
                name = typenamelist[num]  #
                # detail的第一部分
                d1 = k.find('h4')
                d1.find('span').remove()
                d1list = str(d1.text()).split()
                breakfast = d1list[0]  #
                bed = d1list[1]  #
                personnum = d1list[2]  #
                window = d1list[3]  #
                # detail的第二部分（商品价格类型，取消政策）
                d21 = k.find('.left-shrink .room-tag')
                ProductName = str(d21.text())  #
                d22 = k.find('.left-shrink .dt-tag')
                policy = str(d22.text())  #
                # detail的第三部分（价格）
                d3 = k.find('.price')
                d3.find('small').remove()
                price = str(d3.text())  #
                gettime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(roomid, name, breakfast, bed, personnum, window, ProductName, policy, price, gettime,BusinessDate)
                room = {
                    'UnitTypeID': roomid,
                    'UnitTypeName': name,
                    'ProductName':ProductName,
                    'Breakfast': breakfast,
                    'BedType': bed,
                    'PeopleNum': personnum,
                    'CancelRule': policy,
                    'BusinessDate':BusinessDate,
                    'Price': price,
                    'CreateTime': gettime
                }
                # 写入CSV
                try:
                    with open('room.csv', 'a', encoding='utf-8', newline='') as csvfile:
                        fieldnames = ['UnitTypeID', 'UnitTypeName','ProductName', 'Breakfast', 'BedType', 'PeopleNum', 'CancelRule',
                                      'BusinessDate','Price', 'CreateTime']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writerow(room)
                except:
                    print('写入CSV失败')
            num += 1
    finally:
        browser.quit()

    # break
    if (day == 2):
        break
    print('休息30秒')
    time.sleep(30)

