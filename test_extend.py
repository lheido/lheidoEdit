#!/usr/bin/env python
#-*- coding:utf-8 -*-

from extend import extend_manager

class A(object):
	def __init__(self, x):
		self.lang = x
	@extend_manager()
	def foo(self, a, b):
		print a, b
	@extend_manager()
	def foo1(self, x):
		print x*x

a = A("py")
a.foo(1, 2)
a.foo1(1)
