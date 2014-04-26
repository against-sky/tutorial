# -*- coding: utf-8 -*-
from pymongo import *

class ToMongo(object):
	"""docstring for ToMongo"""
	def __init__(self):
		self.client = MongoClient()
		self.db = self.client['baike']

	def insert(self, name, description, url):
		''' there may need to compare the url, not the name
		cause things could have same name'''

		is_exist  = self.db.testData.find_one({'name':name })
		if is_exist == None:
			data = { 'name' :name, 'des' : description, 'url': url }
			self.db.testData.insert(data)
		else:
			print 'game :'+ name + ' is already exists'

		
		