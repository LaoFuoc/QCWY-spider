# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QianchengwuyouItem(scrapy.Item):
    list = ['工作岗位', '城市', '地区', 'more','薪资范围', '平均薪资', '招聘人数', '学历要求', '工作经验',
            '公司名称', '公司类型', '公司规模', '发布时间', '行业' , '公司福利', '职位链接', '职位信息']
    for li in list:
        exec(li + '=scrapy.Field()')

