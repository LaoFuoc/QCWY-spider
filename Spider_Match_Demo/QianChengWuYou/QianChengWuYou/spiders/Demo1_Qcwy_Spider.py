# -*- coding: utf-8 -*-
import scrapy
from ..items import  QianchengwuyouItem
import re


class QcwyspiderSpider(scrapy.Spider):
    name = 'qcwySpider'
    allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,%2B,2,1.html']

    #搜索页
    def parse(self, response):
        url_list = response.xpath('//p/span/a').re('href="(.*?)"')
        for url in url_list:
            yield scrapy.Request(url=url, callback=self.parse_detail)
        next_page  = response.xpath('//*[@id="resultList"]/div[55]/div/div/div/ul/li[8]/a').re('href="(.*?)"')
        if next_page:
            yield scrapy.Request(url=next_page[0], callback=self.parse)

    #详情页
    def parse_detail(self, response):
        item = QianchengwuyouItem()
        item['工作岗位'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/@title').get()
        more= response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()').getall()
        citys = re.split(r'-', more[0].strip())
        item['城市'] = citys[0]
        item['地区'] = citys[-1]
        item['平均薪资'] = None
        hight_edu = ['中专', '中技', '大专', '本科', '硕士', '博士', ]
        item['学历要求'] = '不限'
        item['工作经验'] = ''
        item['招聘人数'] = ''
        item['发布时间'] = ''
        for i in more:
            if '经验' in i:
                item['工作经验'] = i.strip()
            elif i.strip() in hight_edu:
                item['学历要求'] = i.strip()
            elif '招' in i:
                item['招聘人数'] = i.strip()
            elif '发布' in i :
                item['发布时间'] = i.strip()

        item['公司名称'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/@title').get()
        item['公司类型'] = response.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[1]/text()').get()
        item['公司规模'] = response.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[2]/text()').get()
        professional= ''.join(response.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[3]//text()').getall())
        item['专业'] = ''.join([x.strip() for x in professional if x.strip() != ''])
        welfare = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div/span/text()').getall()
        item['公司福利'] = ','.join([x.strip() for x in welfare if x.strip() != ''])
        item['职位链接'] = response.url

        information = response.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div//text()').getall()
        item['职位信息'] = '\n'.join([x.strip() for x in information
                                  if x.strip().replace('?', '').replace('微信分享', '') != '']) # 去除空格，以及部分字

        return item






