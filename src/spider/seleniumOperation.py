from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get('https://m.ctrip.com/webapp/hotel/oversea/hoteldetail/532149.html?atime=20190717')
time.sleep(7)
try:
    btn = browser.find_element_by_xpath('//*[@class="cui-flexbd cui-btns-cancel"]')
    if btn:
        if btn.is_displayed():
            btn.click()
except:
    print("无需点击")
time.sleep(1)
browser.execute_script('window.scrollTo(0, 500)')
detail = browser.find_element_by_xpath('//*[@id="content"]/div/ul/li[2]/div[2]/div[2]/div[2]/div[2]/i')
if detail:
    if detail.is_displayed():
        detail.click()
    else:
        print("详情元素不可见")
else:
    print("未获取到详情元素")
area = browser.find_element_by_xpath('//*[@id="content"]/div/ul/ul[1]/li[1]/div/div')
if area:
    if area.is_displayed():
        area.click()
    else:
        print("区域不可见")
else:
    print("未获取到区域")

room = browser.find_element_by_xpath('//div[@class="hd js_hd"]')
if room:
    title = room.find_element_by_xpath('//div[@class="js_roomtitle"]')
    if title:
        print(title.text)
    else:
        print("未获取到title")
else:
    print("未获取到房间信息")
# browser.close()
# areas = browser.find_element_by_xpath('//*[@class="item sub-price-layout "]')
# for area in areas:
#     area.click()
