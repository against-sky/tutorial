# -*- coding: utf-8 -*-
import codecs
from scrapy.spider import Spider
from scrapy.http import *
from scrapy.selector import Selector
from tutorial.items import DmozItem
from tutorial.ToMongo import ToMongo
from tutorial.ParseBaike import ParseBaike
import re

class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["baidu.com"]
    
    f = codecs.open('./data.txt','r','utf-8')
    urls = []
    for eachline in f:
        urls.append(eachline)
    count = -1

    print 'url len is ' + str(len(urls))
    f.close()    
    
    start_urls = [
        #"http://baike.baidu.com/subview/2188/5215542.htm"
        #"http://baike.baidu.com/view/10795932.htm"
        "http://baike.baidu.com/search/word?word=全民砰砰砰&pic=1&sug=1"
        #"http://baike.baidu.com/view/94220.htm"
        #"http://baike.baidu.com/search/word?word=2货&pic=1&sug=1"
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]
    

    def parse(self, response):

        #first, judge weather crawler is block by the server
        # there may check for the GET status
        if response.url.find('verify')>-1:
            print 'crawler is blocked by the server'
            return
        
        #second, check if the entry searched is exist in Baike
        sel = Selector(response)
        badreq = sel.xpath('//div[@class="direct_holder"]/p/text()').extract()
        notinbaike = '未收录'
        if badreq[0].encode('utf-8').find(notinbaike) > -1:
            print 'this entry is not in baike'
            if self.count < 8549:
                self.count = self.count + 1
                print 'current count is '+ str(self.count)
                yield Request(self.url[self.count],callback=self.parse)
            return

        reg = '<a(.*)href="(.*)"(.*)>(.*)</a>'
        subtext = '游戏'
        #third, if the entry has multiple sub-entries
        lemma_list = sel.xpath('//div[@id="lemma-list"]/ul/li/p/a').extract()
        if lemma_list:
            print 'find lemma_list'
            #it may need to store this page
            for x in lemma_list:
                tmp = re.search(reg, x)
                if tmp.group(4).encode('utf-8').find(subtext) > -1:
                    eUrl = 'http://baike.baidu.com' + tmp.group(2)
                    #print eUrl, tmp.group(4)
                    yield Request(eUrl,callback=self.parse)
        #fourth, if it is truly an entry
        else:
            print 'can not find lemma_list'
            parsebaike =  ParseBaike()
            parsebaike.parse_text(response)

            relatedUrl = sel.xpath('//div[@class="zhixin-list zhixin-list-3"]/div/p/a').extract()
            if relatedUrl:
                print 'find related items'
                for rUrl in relatedUrl:
                    uu = re.search(reg, rUrl)
                    yield Request(uu.group(2),callback=self.parse)  
            else :
                print 'can not find related items'

        if self.count < 8549:
            self.count = self.count + 1
            print 'current count is '+ str(self.count)
            yield Request(self.url[self.count],callback=self.parse)


        
        #print title[0]
        
        #print 'count is '+ str(self.count)
        #self.count = self.count + 1
        #parsebaike = ParseBaike()
        #parsebaike.parse_text(response)
        #f = codecs.open('./data/'+str(self.count-1)+'.txt','w','utf-8')
        #print response.url
        #f.write(response.body.decode('utf-8'))
        #f.close()

        #if self.count >=10:
        #    return 
        #yield Request(self.urls[self.count],callback=self.parse)
        #print self.start_urls
        #print response.body
        #print 'this is meta'
        #print response.meta
        #print 'this is headers'
        #print response.headers
