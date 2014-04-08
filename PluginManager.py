#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import inspect

class PluginManager(object):
	""" class for filter and load plugin """
	
	def __init__ (self, place="extensions", category=None):
		""" category is a dic of class filter """
		self.categories = category 
		path = os.path.abspath(place)
		if os.path.exists(path):
			self.modules = [__import__(module, [module]) for module in os.listdir(path)]
		else:
			print "No plugin folder"
	
	def getPluginsOfCategory(self, *category_names):
		""" return list of plugins class filter by category_name(== parent class) """
		if self.categories:
			result = []
			class_filter = [self.categories[elt] for elt in category_names]
			for module in self.modules:
				for key, value in module.__dict__.iteritems():
					if inspect.isclass(value) and _cmp_parent_class(set(class_filter), set(value.__bases__)):
						result.append(value)
			return result
		else:
			return []
	
	def _cmp_parent_class(self, class_filter, list_class):
		return class_filter & list_class == class_filter
