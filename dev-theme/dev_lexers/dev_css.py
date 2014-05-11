#!/usr/bin/env python
#-*- coding:utf-8 -*-
from PyQt4.QtGui import QColor, QFont
from PyQt4.Qsci import QsciLexerCSS
class Dev_css(QsciLexerCSS):
	def __init__(self, *args):
		super(Dev_css, self).__init__(*args)
		self.setColor(QColor(3,142,42), QsciLexerCSS.IDSelector)
		self.setColor(QColor(170,0,0), QsciLexerCSS.MediaRule)
		self.setColor(QColor(0,0,0), QsciLexerCSS.ExtendedPseudoElement)
		self.setColor(QColor(255,0,0), QsciLexerCSS.UnknownProperty)
		self.setColor(QColor(165,64,157), QsciLexerCSS.PseudoClass)
		self.setColor(QColor(223,146,21), QsciLexerCSS.Important)
		self.setColor(QColor(127,127,0), QsciLexerCSS.AtRule)
		self.setColor(QColor(220,220,220), QsciLexerCSS.CSS3Property)
		self.setColor(QColor(26,26,26), QsciLexerCSS.ExtendedPseudoClass)
		self.setColor(QColor(220,220,220), QsciLexerCSS.CSS2Property)
		self.setColor(QColor(220,220,220), QsciLexerCSS.Default)
		self.setColor(QColor(116,94,206), QsciLexerCSS.Value)
		self.setColor(QColor(85,85,255), QsciLexerCSS.ClassSelector)
		self.setColor(QColor(142,142,142), QsciLexerCSS.Comment)
		self.setColor(QColor(26,26,26), QsciLexerCSS.ExtendedCSSProperty)
		self.setColor(QColor(230,219,116), QsciLexerCSS.SingleQuotedString)
		self.setColor(QColor(85,255,255), QsciLexerCSS.Attribute)
		self.setColor(QColor(26,26,26), QsciLexerCSS.PseudoElement)
		self.setColor(QColor(220,220,220), QsciLexerCSS.CSS1Property)
		self.setColor(QColor(255,0,0), QsciLexerCSS.UnknownPseudoClass)
		self.setColor(QColor(255,85,255), QsciLexerCSS.Tag)
		self.setColor(QColor(230,219,116), QsciLexerCSS.DoubleQuotedString)
		self.setColor(QColor(142,142,142), QsciLexerCSS.Operator)
		self.setPaper(QColor(33,33,33))
		self.setDefaultPaper(QColor(33,33,33))
		
