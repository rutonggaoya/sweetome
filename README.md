# 携程房价爬虫
 爬取携程酒店房价信息数据
1、爬取目标选择：携程手机端网页(m.ctrip.com)
   反爬机制没普通网页端那么强大
2、爬取方法选择：selenium模拟浏览器访问操作 让AJAX传送的房价详细数据得以渲染
3、解析HTML库：pyquery

可以获取从当日起到最多一个月的某一酒店不同房型的定价数据
