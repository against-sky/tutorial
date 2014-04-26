# -*- coding: utf-8 -*-
import string
from scrapy.selector import Selector

class Myparse:
	def parseIntro(self,introduction):
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

	def ohoh(self,x):
		for a in x:
			print a

from HTMLParser import HTMLParser

class BaikeParser(HTMLParser):
	"""docstring for BaikeParser"""
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



		

'''
import urllib2
from sgmllib import SGMLParser
 
class contparse(SGMLParser):
	def __init__(self):
		SGMLParser.__init__(self)
		self.is_a = ""
		self.is_div = ""
		self.name = ""
	def start_a(self, attrs):
		self.is_h4 = 1
	def end_a(self):
		self.is_h4 = ""
	def start_div(self, attrs):
		self.is_div = 1
	def end_div(self, attrs):
		self.is_div = ""
	def handle_data(self, text):
		if self.is_h4 == 1:
			self.name = self.name + text
'''