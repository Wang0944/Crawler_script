# -*- coding:utf-8 -*-
import scrapy
from lxml import etree


class Spider4399Spider(scrapy.Spider):
    name = "spider4399"                     #爬虫名称
    allowed_domains = ["yyxdd.com"]         #爬虫只会在这个网站下采集数据
    start_urls = ["https://m.yyxdd.com/youxigonglue/index-2.html"]      #爬虫开始的采集网站

    def parse(self, response):
        '''
        解析数据的方法
        :param response:    response就是放回的数据，说白了就是网站源码
        :return:        提取的数据
        '''
        # 在攻略页拿到标题和url
        selecters = response.xpath('//div[@class="part_hot_news"]/ul/li')
        for item in selecters:
            my_item={}
            title = item.xpath('./a/div/h2/text()').get()
            url_suffix = item.xpath('./a/@href').get()
            link= response.urljoin(url_suffix)
            img = item.xpath('./a/img/@data-original').get()
            content = ''
            my_item={'title':title,'link':link,'img':img,'content':content}
            request=scrapy.Request(url=link, callback=self.content_parse)   #建立一个请求
            request.meta['my_item'] = my_item  #使用meta方法传到新参数里
            yield request
    #翻页
        next_page = response.xpath('/html/body/div/div[2]/div/div[2]/a[2]')
        if next_page:
            yield response.follow(next_page[0], self.parse)

    def content_parse(self,response):
        my_item= response.meta['my_item']    #meta接受
        html =etree.HTML(response.text)     #获得父标签下的所有文本内容
        all_content=html.xpath('//div[@class="article"]//div[@class="detail" or ./p/img/@src]')
        content_list=[]
        for content in all_content:
            content_list.append(content.xpath('string(.)'))
        my_item['content'] =content_list
        print(my_item)





