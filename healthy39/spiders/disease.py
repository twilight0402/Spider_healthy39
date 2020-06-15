# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.http import Response

from healthy39.utils.util import departList
from healthy39.utils.util import getsubCategoryList
from healthy39.utils.util import getsubCategoryNameList
from healthy39.utils.util import getDiseaseLinks
from healthy39.utils.util import headers
from healthy39.items import Healthy39Item
from healthy39.utils.util import printMsg


class DiseaseSpider(scrapy.Spider):
    name = 'disease'
    allowed_domains = ['39.net']
    start_urls = ['http://jbk.39.net/bw/huxineike_p1/']
    departURL = "http://jbk.39.net/bw/{}_p{}/"  # 一级目录
    subDepartURL = "http://jbk.39.net/bw/{}_p{}/"  # 二级目录|页数
    debug = True

    subdepartList = getsubCategoryList(departList)
    subdepartNameList = getsubCategoryNameList(departList)
    departNameList = ["内科", "外科", "儿科", "妇产科", "男科", "五官科", "皮肤性病", "生殖健康", "中西医结合科",
                      "肝病", "精神心理科", "肿瘤科", "传染科", "老年科", "体检保健科", "成瘾医学科", "核医学科",
                      "急诊科", "营养科"]

    print(departList)
    print(departNameList)
    print(subdepartList)
    print(subdepartNameList)
    printMsg("@获得二级目录", debug)

    def parse(self, response):
        # 一级目录
        for index in range(len(departList)):
            sublist = self.subdepartList[index]
            printMsg(f"# 当前一级目录{self.departNameList[index]}下的子目录：{sublist}", self.debug)

            # 如果没有二级目录，则直接分页迭代一级目录的url
            if 0 == len(sublist):
                index_1 = 1
                while True:
                    url = self.departURL.format(departList[index], index_1)
                    diseaseList, isEnd = getDiseaseLinks(url, headers)
                    printMsg(f"## {departList[index]}没有子目录，直接遍历, URL:{url}", self.debug)
                    printMsg(f"解析到疾病url：{diseaseList}", self.debug)

                    if isEnd:
                        break
                    for diseaseurl in diseaseList:
                        yield Request(url=diseaseurl+"jbzs/", callback=self.parse_disease)
                    index_1 += 1

            # 二级目录
            for name, subDepartName in zip(self.subdepartNameList[index], sublist):
                # 二级目录分页
                index_2 = 1
                printMsg(f"## 子目录：{subDepartName}", self.debug)
                while True:
                    # printMsg(f"\t 页码{index_2}", self.debug)
                    url = self.subDepartURL.format(subDepartName, index_2)
                    # 从这个页面获得各个疾病的入口url，需要解析
                    diseaseList, isEnd = getDiseaseLinks(url, headers)
                    printMsg(f"第{index_2}页的url：{url}", self.debug)
                    printMsg(f"第{index_2}页获得疾病链接如下: {diseaseList}", self.debug)

                    if isEnd:
                        break
                    for diseaseurl in diseaseList:
                        yield Request(url=diseaseurl+"jbzs/", callback=self.parse_disease)
                    index_2 += 1

    def parse_disease(self, response: Response):
        """
        处理一个疾病的所有信息
        :param diseaseType:
        :param response:
        :return:
        """
        disease_info = {}

        # 简介， 名称
        baseinfo = response.xpath("//div[@class='list_left']/div[1]/p[2]/text()").extract_first("")
        diseaseName = response.xpath("//div[@class='disease']/h1/text()").extract_first("")
        disease_info["简介"] = baseinfo.strip()
        disease_info["名称"] = diseaseName.strip()

        root = response.xpath("//div[@class='list_left']/div[@class='disease_box']")
        for disease_box in root:
            disease_basic = disease_box.xpath("ul[@class='disease_basic']")
            for item in disease_basic.xpath("li"):
                title = item.xpath("span[1]/text()").extract_first("").strip()
                value = item.xpath("span[2]/text()").extract_first("").strip()
                if value == "":
                    name = title
                    value = item.xpath("span[2]/a/text()").extract()
                    links = item.xpath("span[2]/a/@href").extract()

                    if not value:
                        printMsg(f"##############{name}, {value}", True)
                    if value and value[-1] == "详细":
                        value = value[:-1]
                    value = ",".join(value)

                    if name == "并发疾病：":
                        for link in links:
                            printMsg(f"### parse_disease: 抛出{diseaseName}的并发疾病{link}jbzs/", self.debug)
                            yield Request(url=link+"jbzs/", callback=self.parse_disease)
                disease_info[title] = value
        item = self.constructItem(disease_info)
        printMsg(f"### parse_disease: 抛出带保存的disease item{item['diseaseName']}", self.debug)
        yield item

    # 将dict转换为item（提取item中的信息）
    def constructItem(self, info: dict):
        item = Healthy39Item()
        item["diseaseName"] = info.get("名称")
        item["baseInfo"] = info.get("简介")  # 简介
        item["aliasName"] = info.get("别名：")  # 别名
        item["isMedicalInsurance"] = info.get("是否属于医保：")  # 是否是医保
        item["position"] = info.get("发病部位：")  # 发病部位
        item["infectivity"] = info.get("传染性：")  # 传染性
        item["MultiplePopulation"] = info.get("多发人群：")  # 多发人群
        item["RelatedSymptoms"] = info.get("相关症状：")  # 相关症状
        item["ConcurrenDiseases"] = info.get("并发疾病：")  # 并发疾病
        item["department"] = info.get("就诊科室：")  # 就诊科室
        item["cureCost"] = info.get("治疗费用：")  # 治疗费用
        item["cureRate"] = info.get("治愈率：")             # 治愈率
        item["curePeriod"] = info.get("治疗周期：")          # 治疗周期
        item["check"] = info.get("相关检查：")               # 相关检查
        item["medical"] = info.get("常用药品：")             # 常用药

        # printMsg(item, self.debug)
        return item


if __name__ == "__main__":
    a = DiseaseSpider()
