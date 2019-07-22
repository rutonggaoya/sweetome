from selenium import webdriver
from pyquery import PyQuery as pq
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

dcap = dict(DesiredCapabilities.PHANTOMJS)
#从USER_AGENTS选一个浏览器头，伪装浏览器
dcap["phantomjs.page.settings.userAgent"] = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1')
# 不载入图片，爬页面速度会快很多
# dcap["phantomjs.page.settings.loadImages"] = Falses
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
browser = webdriver.PhantomJS(executable_path="C:/Python/Scripts/phantomjs.exe", desired_capabilities=dcap)
# # 隐式等待5秒，可以自己调节
# browser.implicitly_wait(5)
# # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
# # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
# browser.set_page_load_timeout(10)
# # 设置10秒脚本超时时间
# browser.set_script_timeout(10)
browser = webdriver.PhantomJS()

# wait = WebDriverWait(browser, 10)
browser.get('https://hotels.ctrip.com/hotel/28374130.html#ctm_ref=hod_hp_hot_dl_n_2_3')
browser.implicitly_wait(20)
# flag = wait.until(EC.presence_of_all_elements_located(By.XPATH,'//*[@id="J_RoomListTbl"]/tbody'))
# flag = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_RoomListTbl"]/tbody/tr[3]/td[4]')))
# print(browser.page_source)
html = browser.page_source
print(html)
doc = pq(html)
items = doc('#hotelRoomBox .htl_room_table J_roomTable #J_RoomListTbl tbody tr')
print(items)
if items:
    for item in items.items():
        roomtype = item.find('.roomtype .room_unfold')
        roomtype.find('span').remove()
        print(roomtype.text())
else:
    print("拿到的房间条目为空")

    # product = {
    #     'image': item.find('.pic .img').attr('data-src'),
    #     'price': item.find('.price').text(),
    #     'deal': item.find('.deal-cnt').text(),
    #     'title': item.find('.title').text(),
    #     'shop': item.find('.shop').text(),
    #     'location': item.find('.location').text()
    # }
    # print(product)
# 获取该床型的所有行数据
# items = browser.find_elements_by_xpath('//*[@id="J_RoomListTbl"]/tbody//*[@brid="2608069"]')
# print(items)
#
# for item in items:
#     style = item.find_element_by_xpath('//*[@class="child_name J_Col_RoomName"]')
#     print(style.text)
#     bedstyle = item.find_element_by_xpath('//*[@class="col_person"]')
#     print(bedstyle.get_attribute('title'))
#     price = item.find_element_by_xpath('//*[@class="base_txtdiv"]')
#     print(price.text)
# 获取所有床型
# UnitTypeNames = browser.find_elements_by_xpath('//*[@class="room_unfold J_show_room_detail"]')
# for i in range(1,len(UnitTypeNames)):
#     unitTypeName = str(UnitTypeNames[i].text)
#     unitTypeName.replace(' ','')
#     print(unitTypeName[:-5])
browser.close()