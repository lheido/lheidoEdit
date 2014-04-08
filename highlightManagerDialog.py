#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class HighlightManagerDialog(QDialog):
	""" Manage user settings """
	def __init__ (self, parent=None):
		super(HighlightManagerDialog, self).__init__(parent)
		
		quitter = QAction("Quitter", self)
		quitter.setShortcut("ctrl+Q")
		quitter.triggered.connect(self.close)
		self.addAction(quitter)
		screen = QDesktopWidget().availableGeometry()
		coef = 0.5
		self.resize(screen.width()*coef, screen.height()*coef)
		size =  self.geometry()
		self.setGeometry((screen.width() - size.width())/2, (screen.height() - size.height())/2, size.width(), size.height())
