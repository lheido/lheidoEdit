#!/usr/bin/env python
#-*- coding:utf-8 -*-
import re
from os import listdir
from os.path import basename, getmtime, abspath, exists
import sys

def load(paths):
	""" Load QsciLexer from PyQt4.Qsci and paths """
	
	default_lexer_module = __import__("PyQt4.Qsci")
	regex = re.compile(r"(?<=QsciLexer)(.+)")
	default_lexers = {}
	new_languages = {}
	for name, lexer in default_lexer_module.Qsci.__dict__.items():
		r = regex.search(name)
		if r and "Custom" not in name:
			default_lexers[r.group(0)] = lexer
	for chemin in paths:
		path = abspath(chemin)
		if exists(path):
			sys.path.append(path)
			regex2 = re.compile(r"(^.+)\.py$")
			lexers_list = [regex2.sub(r"\1", elt) for elt in listdir(path) if regex2.search(elt)]
			for elt in lexers_list:
				tmp = __import__(elt)
				tmp = reload(tmp)
				cl = tmp.__dict__[elt.capitalize()]
				name = regex.search(cl.__bases__[0].__name__)
				name = name.group(0)
				if name not in default_lexers:
					name = cl.__name__
					new_languages[name] = [name.lower()]
				default_lexers[name] = cl
	return default_lexers, new_languages

if __name__ == '__main__':
	load(["dev-theme/dev_lexers", "custom_lexers"])
