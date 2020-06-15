# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Healthy39Item(scrapy.Item):
    diseaseName = scrapy.Field()        # 疾病名称
    baseInfo = scrapy.Field()           # 简介
    aliasName = scrapy.Field()          # 别名
    isMedicalInsurance = scrapy.Field() # 是否是医保
    position = scrapy.Field()           # 发病部位
    infectivity = scrapy.Field()        # 传染性
    MultiplePopulation = scrapy.Field() # 多发人群
    RelatedSymptoms = scrapy.Field()    # 相关症状
    ConcurrenDiseases = scrapy.Field()  # 并发疾病
    department = scrapy.Field()         # 就诊科室
    cureCost = scrapy.Field()           # 治疗费用
    cureRate = scrapy.Field()           # 治愈率
    curePeriod = scrapy.Field()         # 治疗周期
    check = scrapy.Field()              # 相关检查
    medical = scrapy.Field()            # 药品
    department_one = scrapy.Field()     # 一级科室
    department_two = scrapy.Field()     # 二级科室
