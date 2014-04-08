#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
sys.path.append("..")
from extend import extend


@extend(".py")
class myext(object):
	""" Class doc """
	
	def __init__ (self):
		""" Class initialiser """
		self.a = "TEST"
