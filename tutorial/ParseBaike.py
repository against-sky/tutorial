# -*- coding: utf-8 -*-
from pymongo import *
from scrapy.selector import Selector
from HTMLParser import HTMLParser
import codecs
import time

class ParseBaikeIntroduction(object):
	"""docstring for ParseBaikeIntroduction"""
	def parse(self,introduction):
		c = ''
		for x in introduction:
			c = c + x
		#print c
		flag = 0;
		sub = 0
		result = ""
		for x in c:
			if x == '<' and flag == 0:
				flag = 1
			elif x == '>' and flag == 1:
				flag = 0
			elif x == '[':
				sub = 1
			elif x == ']':
				sub = 0
			elif flag == 0 and sub == 0:
				result = result + x
		return result


class ParseBaikeContent(HTMLParser):
	"""docstring for ParseBaikeContent"""
	def __init__(self):
		HTMLParser.__init__(self)
		self.start_section = 0
		self.is_para = 0
		self.is_title = 0
		self.is_sup = 0
		self.content = []
		self.title = []
		self.tmp = ""

	def handle_starttag(self, tag, attrs):
		if tag == "span":
			for name, value in attrs:
				if name == "class" and value == "headline-content":
					self.is_title = 1
		elif tag == "div": 
			for name, value in attrs:
				if name == "class" and value == "para":
					self.is_para = 1
		elif tag == "sup":
			self.is_sup = 1


	def  handle_endtag(self, tag):
		if tag == "span" and self.is_title == 1:
			self.is_title = 0
		elif tag == "div" and self.is_para == 1:
			self.is_para = 0
		elif tag == "sup":
			self.is_sup = 0

	def  handle_data(self, data):
		if self.is_title == 1:
			self.title.append(data)
			#print data
			if self.start_section == 0:
				self.start_section = 1
			else :
				self.content.append(self.tmp)
				self.tmp = ""

		elif self.is_para == 1:
			if self.is_sup == 0:
				self.tmp = self.tmp + data
			#print data
		



class ParseBaike(object):
	"""docstring for ParseBaike"""
	def __init__(self):
		self.client = MongoClient()
		self.db = self.client['baike']

	def create_entry(self, url, name, introduction):
		is_exist  = self.db.baidu.find_one({ 'url':url })
		if is_exist == None:
			data = { 'name' :name, 'des' : introduction, 'url': url }
			self.db.BaiduBaike.insert(data)
			print 'create entry for ' + name
			print 'url is ' + url
			return 1
		else:
			print 'game :'+ name + ' is already exists'
			print 'url is ' + url
			return 0

	def update_entry(self, sub_titles, sub_contents, url):
		
		dic = []
		for x in xrange(0,len(sub_contents)):
			prop = { 'title': sub_titles[x],'content':sub_contents[x] }
			dic.append(prop)
		#print dic
		self.db.BaiduBaike.update({'url': url},{ '$push': { 'property' : { '$each' : dic}}})

	def parse_text(self, html_data):
		url = html_data.url.split('?')[0]
		print url
		sel = Selector(html_data)
		tmp = sel.xpath('//div[@class="lemmaTitleH1"]/text()').extract()
		title = tmp[0]
		print 'title in parseBaike' + title
		tmp_intro = sel.xpath('//div[@class="card-summary-content"]/*').extract()
		tmp_content = sel.xpath('//div[@class="lemma-main-content rainbowlemma--"]/*').extract()
		parse_intro = ParseBaikeIntroduction()
		introduction = parse_intro.parse(tmp_intro)

		val = self.create_entry(url, title, introduction)
		if val == 0:
			print 'return in parse_text'
			return
		parse_content = ParseBaikeContent()
		temp = ''
		for text in tmp_content:
			temp = temp + text
		parse_content.feed(temp)

		sub_titles = parse_content.title
		sub_contents = parse_content.content
		self.update_entry(sub_titles, sub_contents, url)
		
		'''
		print title
		print introduction

		for x in xrange(0,len(sub_contents)):
			print sub_titles[x]
			print sub_contents[x]
		print len(sub_titles),len(sub_contents)
		'''

		ctime = str(time.time()*10).split('.')
		f = codecs.open('./data/'+title+'_'+ctime[0]+'.html','w','utf-8')
		f.write(html_data.body.decode('utf-8'))
		f.close()


