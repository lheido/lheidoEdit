#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from MainWindow import MainWindow

class LheidoEdit(QApplication):
	""" LheidoEdit app class extend QApplication """
	
	def __init__ (self, argv):
		QApplication.__init__(self, argv)
		self.__mainWin = MainWindow()
		with open("dev_theme.css") as t:
			dev_theme = t.read()
		self.setStyleSheet(dev_theme)
	
	def run(self):
		self.__mainWin.show()
		self.exec_()

if __name__ == '__main__':
	app = LheidoEdit(sys.argv)
	app.run()
