#!/usr/bin/env python
#-*- coding:utf-8 -*-
from PyQt4.QtGui import QColor, QFont
from PyQt4.Qsci import QsciLexerPython
class Dev_python(QsciLexerPython):
	def __init__(self, *args):
		super(Dev_python, self).__init__(*args)
		self.setColor(QColor(84,84,84), QsciLexerPython.Comment)
		self.setColor(QColor(230,219,116), QsciLexerPython.SingleQuotedString)
		self.setColor(QColor(246,38,113), QsciLexerPython.Keyword)
		self.setColor(QColor(200,42,42), QsciLexerPython.UnclosedString)
		self.setColor(QColor(142,182,255), QsciLexerPython.HighlightedIdentifier)
		self.setColor(QColor(230,219,116), QsciLexerPython.TripleDoubleQuotedString)
		self.setColor(QColor(139,120,206), QsciLexerPython.Number)
		self.setColor(QColor(164,223,46), QsciLexerPython.ClassName)
		self.setColor(QColor(220,220,220), QsciLexerPython.Default)
		self.setColor(QColor(164,223,46), QsciLexerPython.FunctionMethodName)
		self.setColor(QColor(230,219,116), QsciLexerPython.DoubleQuotedString)
		self.setColor(QColor(142,142,142), QsciLexerPython.Operator)
		self.setColor(QColor(84,84,84), QsciLexerPython.CommentBlock)
		self.setColor(QColor(220,220,220), QsciLexerPython.Identifier)
		self.setColor(QColor(200,200,142), QsciLexerPython.Decorator)
		self.setColor(QColor(230,219,116), QsciLexerPython.TripleSingleQuotedString)
		self.setPaper(QColor(33,33,33))
		self.setDefaultPaper(QColor(33,33,33))
	
	def keywords(self, ens):
		if ens == 1:
			return "and as assert break class continue def del elif else except exec finally for from global if import in is lambda None True False not or pass print raise return try while with yield"
		elif ens == 2:
			return "self abs divmod input open staticmethod all enumerate int ord str any eval isinstance pow sum basestring execfile issubclass super bin file iter property tuple bool filter len range type bytearray float list raw_input unichr callable format locals reduce unicode chr frozenset long reload vars classmethod getattr map repr xrange cmp globals max reversed zip compile hasattr memoryview round __import__ complex hash min set apply delattr help next setattr buffer dict hex object slice coerce dir id oct sorted intern"
