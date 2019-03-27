# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Tencent.items import tencentSpiderItem

class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=0#a']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )
    #匹配每一页规则
    pagelink = LinkExtractor(allow=('start=\d+'))
    print(pagelink)


    #匹配详情页规则
    contentlink = LinkExtractor(allow=('id=\d+&keywords=&tid=0&lid=0'))

    rules = (
        Rule(pagelink, follow=True),
        Rule(contentlink, callback='parse_item', follow=True)
    )



    def parse_item(self, response):
        # print(response.url)
        #岗位名称
        title = response.xpath("//tr[@class='h']/td/text()").extract()[0]
        #工作地点
        place = response.xpath("//tr[@class='c bottomline']/td[1]/text()").extract()[0]
        #职位类别
        type = response.xpath("//tr[@class='c bottomline']/td[2]/text()").extract()[0]
        #招聘人数
        number = response.xpath("//tr[@class='c bottomline']/td[3]/text()").extract()[0]
        #工作职责
        duty = response.xpath("//tr[3]/td/ul/li/text()").extract()
        duty = "".join(duty)
        #工作要求
        req = response.xpath("//tr[4]/td/ul/li/text()").extract()
        req = "".join(req)

        # print(title)
        # print(place)
        # print(type)
        # print(number)
        # print(duty)
        # print(req)

        item = tencentSpiderItem()
        item['title'] = title
        item['place'] = place
        item['type'] = type
        item['number'] = number
        item['duty'] = duty
        item['req'] = req

        print(item)
        yield item