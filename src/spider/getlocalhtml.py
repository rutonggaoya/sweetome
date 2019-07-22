import csv
import datetime
import os
from pyquery import PyQuery as pq

f = open("source.html","r",encoding='utf-8')
html = f.read()
f.close()
doc = pq(html)

# 创建CSV
# if os.path.exists("localroom.csv"):
#     os.remove('localroom.csv')
# with open('localroom.csv', 'w', encoding='utf-8', newline='') as csvfile:
#     fieldnames = ['UnitTypeID', 'UnitTypeName', 'Breakfast', 'BedType', 'PeopleNum', 'CancelRule', 'Price', 'CreateTime']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()

#获取酒店名字
hotelname = doc('.des.js_honor_desc h1 span').text()
#获取所有房型的ID和名字
roomtypes = doc('.cell-star.room-bd.js_show_baseroom')
typelist = []
for i in roomtypes.items():
    typeid = i.attr('data-bid')
    typename = i.find('h3')
    typename.find('span').remove()
    roomtype = {
        'typeid':typeid,
        'typename':typename.text()
    }
    typelist.append(roomtype)
print("共有房型数：",len(typelist))

#获取每个房型下面的详细列表
allroomtypes = doc('.dl-room-type.js_roomlist .sub-romm.js_childroomlist')
num = 0
for j in allroomtypes.items():
    # roomid = j.find('.item.sub-price-layout ').attr('data-roomid')
    details = j.find('.item.sub-price-layout ')
    # details = j.find('.cell-star.room--space3')
    for k in details.items():
        typeid = typelist[num]['typeid']  #
        typename = typelist[num]['typename'] #
        roomid = str(k.attr('data-roomid'))  #
        #detail的第一部分(早饭，床型，人数，窗户)
        d1 = k.find('h4')
        d1.find('span').remove()
        d1list = str(d1.text()).split()
        breakfast = d1list[0]#
        bed = d1list[1]#
        personnum = d1list[2]#
        window = d1list[3]#
        #detail的第二部分（商品价格类型，取消政策）
        d21 = k.find('.left-shrink .room-tag')
        ProductName = str(d21.text())#
        d22 = k.find('.left-shrink .dt-tag')
        policy = str(d22.text())#
        #detail的第三部分（价格）
        d3 = k.find('.price')
        d3.find('small').remove()
        price = str(d3.text())#
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(hotelname,typeid,typename,roomid,breakfast,bed,personnum,window,ProductName,policy,price)
        room = {
            # 'HotelID': name,
            'HotelName': hotelname,
            'RoomTypeID': typeid,
            'RoomTypeName': typename,
            'RoomID': roomid,
            'ProductName': ProductName,
            'Breakfast': breakfast,
            'BedType': bed,
            'PeopleNum': personnum,
            'CancelRule': policy,
            # 'BusinessDate': BusinessDate,
            'Price': price,
            # 'CreateTime': gettime
}
        #写入excel
        # try:
        #         #     with open('localroom.csv', 'a', encoding='utf-8', newline='') as csvfile:
        #         #         fieldnames = ['UnitTypeID', 'UnitTypeName', 'Breakfast', 'BedType', 'PeopleNum', 'CancelRule', 'Price', 'CreateTime']
        #         #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #         #         writer.writerow(room)
        #         # except:
        #         #     print('写入CSV失败')
    num += 1
