# # -*- coding: utf-8 -*-
# from urllib import parse
# import requests
# import re
# import json
#
# import scrapy
# from scrapy import Request
# from scrapy import Selector
# from scrapySecondHandHousing.items import LianJiaItem
#
# # 负责解析和抓取逻辑就行了
# class LianJiaSpider(scrapy.Spider):
#     name = 'LianJia'
#     allowed_domains = ['lianjia.com']
#     start_urls = ['https://su.lianjia.com/ershoufang/pg1/']
#     # start_urls = ['https://bj.lianjia.com/ershoufang/pg1/']
#     # start_urls = ['https://sh.lianjia.com/ershoufang/pg1/']
#
#     base_url = 'https://su.lianjia.com'
#     # base_url = 'https://bj.lianjia.com'
#     # base_url = 'https://sh.lianjia.com'
#
#     # 区域
#     def parse(self, response):
#         area_url = response.xpath('//div[@data-role="ershoufang"]/div[1]/a/@href').extract()
#         for url in area_url:
#             yield Request(url=self.base_url + url, callback=self.parse_region)
#
#     # 区域里的所有小地区
#     def parse_region(self, response):
#         local_url = response.xpath('//div[@data-role="ershoufang"]/div[2]/a/@href').extract()
#         for url in local_url:
#             yield Request(url=self.base_url + url + 'pg1/', callback=self.parse_detail_page)
#
#     # 获取所有页
#     def parse_detail_page(self, response):
#         total_page = json.loads(response.xpath('//div[@class="page-box fr"]/div[1]/@page-data').extract()[0])[
#             "totalPage"]
#         if total_page:
#             for i in range(1, total_page + 1):
#                 yield Request(url=response.url[:-2] + str(i) + '/', callback=self.parse_detail)
#
#     # 一个区域里的一个地方的列表页
#     def parse_detail(self, response):
#         detail_url = response.xpath('//div[@class="title"]/a/@href').extract()
#         for url in detail_url:
#             yield Request(url=url, callback=self.parse_item)
#
#     # 详情页解析
#     def parse_item(self, response):
#         item = LianJiaItem()
#
#         item['title'] = response.xpath('//h1/@title').extract()[0]
#         item['url'] = response.url
#
#         # ?就是非贪婪匹配'单引号
#         item['house_id'] = re.findall(r"houseId:'(.*?)',", response.text)[0]
#         item['city_name'] = re.findall(r"cityName:'(.*?)',", response.text)[0]
#         item['register_time'] = re.findall(r"registerTime:'(.*?)',", response.text)[0]  # 房屋年限
#
#         create_time = response.xpath("//*[@id='introduction']/div/div/div[2]/div[2]/ul/li[1]/span[2]/text()").extract()[0]
#         item['create_time'] = create_time
#
#         update_time = response.xpath("//*[@id='introduction']/div/div/div[2]/div[2]/ul/li[3]/span[2]/text()").extract()[0]
#         item['update_time'] = update_time
#
#         item['house_type'] = re.findall(r"houseType:'(.*?)',", response.text)[0]
#         item['positions'] = re.findall(r"resblockPosition:'(.*?)',", response.text)[0]
#         item['longitude'] = item['positions'].split(',')[0]
#         item['latitude'] = item['positions'].split(',')[1]
#
#         item['area'] = re.findall(r"area:'(.*?)',", response.text)[0]
#         item['total_price'] = re.findall(r"totalPrice:'(.*?)',", response.text)[0]
#         item['avg_price'] = re.findall(r"price:'(.*?)',", response.text)[0]
#         item['community'] = re.findall(r"resblockName:'(.*?)',", response.text)[0]
#
#         base_datail = response.xpath('//*[@id="introduction"]//ul/li/text()').extract()
#         item['layout'] = base_datail[0]
#         item['floor'] = base_datail[1]
#         # item['area'] = base_datail[2][:-1]
#
#         if item['house_type'] == '别墅':
#             item['direction'] = base_datail[4]
#             item['decorate'] = base_datail[6]
#
#         else:
#             item['design'] = base_datail[3]
#             item['direction'] = base_datail[6]
#             item['decorate'] = base_datail[8]
#             item['lift'] = base_datail[10]
#             item['lift_proportion'] = base_datail[9]
#
#         # item['total_price'] = response.xpath('//span[@class="total"]/text()').extract()[0]
#         # item['avg_price'] = response.xpath('//span[@class="unitPriceValue"]/text()').extract()[0]
#
#         item['region'] = response.xpath('//span[@class="info"]/a[1]/text()').extract()[0]
#         item['locals'] = response.xpath('//span[@class="info"]/a[2]/text()').extract()[0]
#         # item['community'] = response.xpath('//div[@class="communityName"]/a[1]/text()').extract()[0]
#
#         yield item
#
