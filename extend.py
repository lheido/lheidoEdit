#!/usr/bin/env python
#-*- coding:utf-8 -*-
import re
import os
import sys
from inspect import isclass

class Extend(object):
	def __init__(self, **kwargs):
		self.lang = kwargs["lang"]
		self.override = kwargs["over"]
		self.name = kwargs["name_"]
		self.obj = kwargs["obj_"]
	
def extend(language=None, override=None, name=None):
	""" 
User obj definition decorator 
	how to use:
		@extend(language, override, name)
		class MyClass(parent)
	the decorator return an instance of Extend that
	contains the class defined.
	if langage is empty:
		extend base class
	else:
		extend editor functionnalities for langage with name of base
		methode
	if override: # if obj is function
		overrided methode
	else:
		new functionnalities
	"""
	def decorator(obj):
		""" obj is function or class def """
		return Extend(lang=language, over=override, name_=name, obj_=obj)
	return decorator

def extend_manager(place="extensions", mth=True):
	""" 
Base obj defintion decorator
	how to use:
		@extend_manager("path/to/extension/folder", False)
		class LheidoEditClass(parent)
		or
		@extend_manager("path/to/extension/folder")
		def methode(self, *args)
	extend_manager will check the extensions folder("extensions by
	default") and will replace the current class|methode by the 
	appropriate extension.
	if mth:
		methode decorate with extend_manager is replaced by function
		who check language and call appropriate function
		if you want to override the default methode, just define a
		class inherit from baseclass (ex: Editor)
	else: decorate class 
	 """
	def decorator(obj):
		path = os.path.abspath(place)
		if os.path.exists(path):
			sys.path.append(path)
			regex = re.compile(r"(^.+)\.py$")
			extensions_list = [regex.sub(r"\1", elt) for elt in os.listdir(path) if regex.search(elt)]
			user_extensions = []
			for ext in extensions_list:
				tmp = __import__(ext)
				tmp = reload(tmp)
				for key, value in tmp.__dict__.items():
					if isinstance(value, Extend):
						user_extensions.append(value)
			if mth: # obj is methode
				obj_name = obj.__name__
				def wrapper(self, **kwargs):
					funs = {ext.lang: ext.obj for ext in user_extensions if ext.override and ext.name == obj_name}
					if hasattr(self, "lang") and self.lang in funs: funs[self.lang](self, **kwargs)
					else: obj(self, **kwargs)
				return wrapper
			else: # obj is class definition
				for ext in user_extensions:
					if isclass(ext.obj) and issubclass(ext.obj, obj):
						return ext.obj
				return obj
	return decorator
