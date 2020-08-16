# -*- coding: utf-8 -*-
import scrapy
from ..items import  QianchengwuyouItem


class QcwyspiderSpider(scrapy.Spider):
    name = 'qcwySpider'
    allowed_domains = ['51job.com']
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,1.html']

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
        item['more']    = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()').getall()
        item['薪资范围'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/strong/text()').get()
        item['公司名称'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/@title').get()
        item['公司类型'] = response.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[1]/text()').get()
        item['公司规模'] = response.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[2]/text()').get()
        item['行业']     = response.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[3]//text()').getall()
        item['公司福利'] = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div/span/text()').getall()
        item['职位链接'] = response.url
        item['职位信息'] = response.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div//text()').getall()

        return item
