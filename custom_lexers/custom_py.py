#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4.QtGui import QColor, QFont
from PyQt4.Qsci import QsciLexerPython

#~ enum { 
  #~ Default = 0, Comment = 1, Number = 2, 
  #~ DoubleQuotedString = 3, SingleQuotedString = 4, Keyword = 5, 
  #~ TripleSingleQuotedString = 6, TripleDoubleQuotedString = 7, ClassName = 8, 
  #~ FunctionMethodName = 9, Operator = 10, Identifier = 11, 
  #~ CommentBlock = 12, UnclosedString = 13, HighlightedIdentifier = 14, 
  #~ Decorator = 15 
#~ }


class Custom_py(QsciLexerPython):
	def __init__(self, *args):
		super(Custom_py, self).__init__(*args)
		self.setColor(QColor("#FFFFFF"), QsciLexerPython.Default)
		self.setColor(QColor(84, 84, 84), QsciLexerPython.Comment)
		self.setColor(QColor("#8B78CE"), QsciLexerPython.Number)
		self.setColor(QColor("#E6DB74"), QsciLexerPython.DoubleQuotedString)
		self.setColor(QColor("#E6DB74"), QsciLexerPython.SingleQuotedString)
		self.setColor(QColor("#F62671"), QsciLexerPython.Keyword)
		self.setColor(QColor("#E6DB74"), QsciLexerPython.TripleDoubleQuotedString)
		self.setColor(QColor("#E6DB74"), QsciLexerPython.TripleSingleQuotedString)
		self.setColor(QColor("#A4DF2E"), QsciLexerPython.ClassName)
		self.setColor(QColor("#A4DF2E"), QsciLexerPython.FunctionMethodName)
		self.setColor(QColor("#FFFFFF"), QsciLexerPython.Operator)
		self.setColor(QColor("#FFFFFF"), QsciLexerPython.Identifier)
		self.setColor(QColor(0, 0, 0), QsciLexerPython.CommentBlock)
		self.setColor(QColor(0, 0, 0), QsciLexerPython.UnclosedString)
		self.setColor(QColor(142, 182, 255), QsciLexerPython.HighlightedIdentifier)
		self.setColor(QColor(200, 200, 142), QsciLexerPython.Decorator)
		self.setPaper(QColor(33,33,33)) # bg uniquement sous les charactères
		self.setDefaultPaper(QColor(33,33,33)) # global bg
		#~ self.setEolFill(True) # bg pour le reste
	
	def keywords(self, ens):
		if ens == 1:
			return "and as assert break class continue def del elif else except exec finally for from global if import in is lambda None True False not or pass print raise return try while with yield"
		elif ens == 2:
			return "self abs divmod input open staticmethod all enumerate int ord str any eval isinstance pow sum basestring execfile issubclass super bin file iter property tuple bool filter len range type bytearray float list raw_input unichr callable format locals reduce unicode chr frozenset long reload vars classmethod getattr map repr xrange cmp globals max reversed zip compile hasattr memoryview round __import__ complex hash min set apply delattr help next setattr buffer dict hex object slice coerce dir id oct sorted intern"
