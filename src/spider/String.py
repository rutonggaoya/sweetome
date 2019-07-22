# str = "特价单人间详情代理"
# str1 = "20m² 大床 无窗"
# print(str1.split(' '))
# print(str1[0:-1])
# print(str[:-4])


import datetime

from fake_useragent import UserAgent

s = '<div class="cell-star room-column room--space  " data-roomid="30037508" data-shadowid="0" data-index="1"><div>'
day=1
date = int(datetime.datetime.now().strftime('%Y%m%d'))+day
url = 'https://m.ctrip.com/webapp/hotel/hoteldetail/532149.html?days=1&atime='+str(date)
print(url)
res = datetime.datetime.strptime(str(date), "%Y%m%d").strftime('%Y-%m-%d')
print(res)
print(type(res))

ua = UserAgent()

print(ua.random)
# for i in ua.data.items():
#     print(i)
