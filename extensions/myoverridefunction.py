#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
sys.path.append("..")
from extend import extend

def foo1():
	return 4

def foo2():
	return 2

@extend("py", True, "foo")
def first(self, a, b):
	print "{0}{1}".format(foo1(), foo2())

@extend("py", True, "foo1")
def second(self, x):
	print x + x
