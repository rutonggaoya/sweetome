import csv
import datetime
import os
import time
import requests
import random
from selenium import webdriver
# 抓取主页数据(爬下来的网页class名字有的有变动！！！！！！！！！)
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from fake_useragent import UserAgent
import base64

PROXY_POOL_URL = 'http://localhost:5555/random'


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


# 创建CSV
def createCSV(hotelid):
    if os.path.exists(hotelid + "room.csv"):
        os.remove(hotelid + 'room.csv')
    with open(hotelid + 'room.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['HotelID', 'HotelName', 'RoomTypeID', 'RoomTypeName', 'RoomID',
                      'ProductName', 'Breakfast', 'BedType',
                      'PeopleNum',
                      'CancelRule',
                      'BusinessDate', 'Price', 'CreateTime']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


# 获取房间数据
def getResult(days, hotelid):
    # 定义phantomJS的一些设置和headers
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    # 从USER_AGENTS选一个浏览器头，伪装浏览器，下面可以更换的请求头
    #   Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36
    #   Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)
    #   MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1
    ua = UserAgent()
    myua = ua.random
    # myua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    print("此次USER-AGENT为：", myua)
    dcap["phantomjs.page.settings.userAgent"] = myua
    # 不载入图片，爬页面速度会快很多
    dcap["phantomjs.page.settings.loadImages"] = False
    # 设置代理
    myproxy = get_proxy()
    print("此次代理为：", myproxy)
    service_args = [
        # '--proxy=123.115.229.135:8060',
        '--proxy=' + myproxy,  # 代理 IP：prot    （eg：192.168.0.28:808）
        '--proxy-type=https',  # 代理类型：http/https/socks5
        '--load-images=no',  # 关闭图片加载（可选）
        '--disk-cache=yes',  # 开启缓存（可选）
        '--ignore-ssl-errors=true'  # 忽略https错误（可选）
    ]

    # 创建phantomjs网页驱动器
    browser = webdriver.PhantomJS(desired_capabilities=dcap, service_args=service_args)
    # browser = webdriver.PhantomJS()
    # 等待响应时间为10s
    wait = WebDriverWait(browser, 8)

    try:
        print("共抓取", days, "天信息！")
        # 抓取从当天开始
        for day in range(days):
            print('第', day, '天抓取：')

            # url = 'https://m.ctrip.com/webapp/hotel/hoteldetail/1451725.html?atime=20190718&daylater=0&days=1&contrl=0&pay=0&discount=&latlon=&listindex=4&userLocationSearch=false#fromList'
            # url后缀
            date = int(datetime.datetime.now().strftime('%Y%m%d')) + day
            BusinessDate = datetime.datetime.strptime(str(date), "%Y%m%d").strftime('%Y-%m-%d')
            url = 'https://m.ctrip.com/webapp/hotel/hoteldetail/' + hotelid + '.html?days=1&atime=' + str(
                date) + '&contrl=0&num=undefined&biz=undefined'
            # url = 'https://m.ctrip.com/webapp/hotel/hoteldetail/532149.html?days=1&atime=20190719&contrl=0&num=undefined&biz=undefined&ctm_ref=ch5_hp_bs_lst'
            print(url)

            # selenium开始解析网页
            browser.get(url)
            # 判断页面中有无此元素,有则页面加载成功
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                           '#content > div > ul > li:nth-child(2) > div.cell-star.room-column.room--space > div.cell-star.room-bd.js_show_baseroom > h3')))
                print('加载成功')
            except:
                print("获取表格元素失败")
                continue

            html = browser.page_source
            doc = pq(html)

            # 获取酒店名字
            hotelname = doc('.des.js_honor_desc h1 span').text()
            # 获取所有房型的ID和名字
            roomtypes = doc('.cell-star.room-bd.js_show_baseroom')
            typelist = []
            for i in roomtypes.items():
                typeid = i.attr('data-bid')
                typename = i.find('h3')
                typename.find('span').remove()
                roomtype = {
                    'typeid': typeid,
                    'typename': typename.text()
                }
                typelist.append(roomtype)
            print("共有房型数：", len(typelist))

            # 获取每个房型下面的详细列表
            allroomtypes = doc('.dl-room-type.js_roomlist .sub-romm.js_childroomlist')
            num = 0
            for j in allroomtypes.items():
                details = j.find('.item.sub-price-layout ')
                for k in details.items():
                    typeid = typelist[num]['typeid']  #
                    typename = typelist[num]['typename']  #
                    roomid = str(k.attr('data-roomid'))  #
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
                    d3 = k.find('span.price')
                    d3.find('small').remove()
                    price = str(d3.text())  #
                    gettime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(hotelid, hotelname, typeid, typename, roomid, breakfast, bed, personnum, window, ProductName,
                          policy,
                          price, gettime,
                          BusinessDate)
                    room = {
                        'HotelID': hotelid,
                        'HotelName': hotelname,
                        'RoomTypeID': typeid,
                        'RoomTypeName': typename,
                        'RoomID': roomid,
                        'ProductName': ProductName,
                        'Breakfast': breakfast,
                        'BedType': bed,
                        'PeopleNum': personnum,
                        'CancelRule': policy,
                        'BusinessDate': BusinessDate,
                        'Price': price,
                        'CreateTime': gettime
                    }
                    # 写入CSV
                    try:
                        with open(hotelid + 'room.csv', 'a', encoding='utf-8', newline='') as csvfile:
                            fieldnames = ['HotelID', 'HotelName', 'RoomTypeID', 'RoomTypeName', 'RoomID',
                                          'ProductName', 'Breakfast', 'BedType',
                                          'PeopleNum',
                                          'CancelRule',
                                          'BusinessDate', 'Price', 'CreateTime']
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writerow(room)
                    except:
                        print('写入CSV失败')
                num += 1
            # break
            if (day == days - 1):
                break

            t = random.randint(30, 60)
            print('休息', t, '秒')
            time.sleep(t)

    finally:
        browser.quit()


if __name__ == '__main__':
    hotelid = '4592984'
    createCSV(hotelid)
    getResult(2, hotelid)
