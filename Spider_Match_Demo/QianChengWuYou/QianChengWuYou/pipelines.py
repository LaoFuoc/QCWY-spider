# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import re

class QianchengwuyouPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient()
        db = client['51Job']
        self.collection = db.CrawlScrapy

    def process_item(self, item, spider):

        global avgs
        more = item['more']
        citys = re.split(r'-', more[0].strip())
        item['城市'] = citys[0]
        item['地区'] = citys[-1]

        salary = item['薪资范围']
        try:
            if '万/月' in salary:
                sala1 = re.split(r'-', salary[:-3])
                min = float(sala1[0])
                max = float(sala1[1])
                avgs = int(round((min + (max - min) * 0.4) * 10000, 0))
            if '万/年' in salary:
                sala2 = re.split(r'-', salary[:-3])
                min = float(sala2[0])
                max = float(sala2[1])
                avgs = int(round((min + (max - min) * 0.4) / 12 * 10000, 0))
            if '千/月' in salary:
                sala3 = re.split(r'-', salary[:-3])
                min = float(sala3[0])
                max = float(sala3[1])
                avgs = int(round((min + (max - min) * 0.4) * 1000, 0))
            if '元/天' in salary:
                sala4 = re.split(r'-', salary[:-3])
                avgs = int(round(float(sala4[0]) * 30, 0))
            item['平均薪资'] = int(avgs)
        except:
            item['平均薪资'] = '薪资面议'

        hight_edu = ['中专', '中技', '大专', '本科', '硕士', '博士', ]
        item['学历要求'] = '不限'
        item['工作经验'] = '无工作经验'
        item['招聘人数'] = ''
        item['发布时间'] = ''
        for i in more:
            if '经验' in i:
                item['工作经验'] = i.strip()
            elif i.strip() in hight_edu:
                item['学历要求'] = i.strip()
            elif '招' in i:
                item['招聘人数'] = i.strip()
            elif '发布' in i:
                item['发布时间'] = i.strip()

        professional  = ''.join(item['行业'])
        item['行业'] = ''.join([x.strip() for x in professional if x.strip() != ''])

        welfare = item['公司福利']
        item['公司福利'] = ','.join([x.strip() for x in welfare if x.strip() != ''])

        information = item['职位信息']
        item['职位信息'] = '\n'.join([x.strip() for x in information if x.strip().replace('?', '').replace('微信分享', '') != ''])

        del item['more']
        text = dict(item)
        self.collection.insert(text)

        return  item

