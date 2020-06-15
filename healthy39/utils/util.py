import requests
from bs4 import BeautifulSoup
import os
import pickle
import pymysql
from healthy39.items import Healthy39Item

departList = ["neike", "waike", "erke", "fuchanke", "nanke", "wuguanke", "pifuxingbing",
              "shengzhijiankang","zhongxiyijieheke", "ganbing", "jingshenxinlike", "zhongliuke", "chuanrangke",
              "laonianke", "tijianbaojianke", "chengyinyixueke", "heyixueke", "jizhenke", "yingyangke"]
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}
conn = pymysql.connect(host="localhost", user ="root", password="123456", database="healthy39"
                           , charset="utf8")


def getsubCategoryList(kindList, outputfile="subcategorylist.pkl"):
    """
    获得二级目录的拼音
    :param kindList:
    :param outputfile:
    :return:
    """
    if os.path.exists(outputfile):
        with open(outputfile, "rb") as file:
            res = pickle.load(file)
            print("load subcategorylist")
    else:
        res = []
        for kind in kindList:
            departes = []
            response = requests.get("http://jbk.39.net/bw/{}_t1/".format(kind), headers=headers)
            html_doc = response.text

            tree = BeautifulSoup(html_doc, "html.parser")
            li = tree.select(".type_subscreen_unit")

            if len(li) != 0:
                li = li[0]
                a_links = li.select("a")

                for link in a_links:
                    subcate = link.attrs["href"]
                    subcate = subcate.split("/")[2].split("_")[0]

                    departes.append(subcate)
            res.append(departes)

        with open(outputfile, "wb") as file:
            pickle.dump(res, file)
            print("dump subcategorylist")
    return res


def getsubCategoryNameList(kindList, outputfile="subcategoryNamelist.pkl"):
    """
    获得二级目录的中文名称
    :param kindList:
    :param outputfile:
    :return:
    """
    if os.path.exists(outputfile):
        with open(outputfile, "rb") as file:
            res = pickle.load(file)
            print("load subcategoryNamelist")
    else:
        res = []
        for kind in kindList:
            departes = []
            response = requests.get("http://jbk.39.net/bw/{}_t1/".format(kind), headers=headers)
            html_doc = response.text

            tree = BeautifulSoup(html_doc, "html.parser")
            li = tree.select(".type_subscreen_unit")

            if len(li) != 0:
                li = li[0]
                a_links = li.select("a")

                for link in a_links:
                    subcate = link.text
                    departes.append(subcate)
            res.append(departes)

        with open(outputfile, "wb") as file:
            pickle.dump(res, file)
            print("dump subcategoryNamelist")
    return res


def getDiseaseLinks(url, headers):
    response = requests.get(url, headers=headers)
    tree = BeautifulSoup(response.text, "html.parser")
    linklist = tree.select(".result_item")
    linkList = []
    isEnd = False

    if 1 == len(linklist):
        content = linklist[0].select("p")[0].text
        if content.count("抱歉") >= 1:
            isEnd = True

    for link in linklist:
        tabtype = link.select("span")[0].text
        if tabtype == "疾病":
            linkList.append(link.select("a")[0].attrs["href"])
    return linkList, isEnd


def saveItems(item: Healthy39Item):
    cursor = conn.cursor()
    sql = "INSERT INTO disease VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, NULL);"
    cursor.execute(sql, (item["diseaseName"], item["baseInfo"], item["aliasName"], item["isMedicalInsurance"], item["position"],
                   item["infectivity"], item["MultiplePopulation"], item["RelatedSymptoms"], item["ConcurrenDiseases"],
                   item["department"], item["cureCost"], item["cureRate"], item["curePeriod"],
                   item["check"], item["medical"]))
    conn.commit()
    cursor.close()


def printMsg(msg, flag):
    if flag:
        print(msg)


if __name__ == "__main__":
    res = getsubCategoryList(departList)
    print(res)