#!/usr/bin/env python
#-*- coding:utf-8 -*-
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import QsciScintilla, QsciAPIs
import load_lexer

class Sample(QsciScintilla):
	def __init__(self):
		super(Sample, self).__init__()
		self.setUtf8(True)
		self.font = QFont()
		self.font.setFamily('Ubuntu Mono')
		self.font.setFixedPitch(True)
		self.font.setPointSize(11)
	
	def open_sample(self, name):
		try:
			with open("highlightManager_sample/{0}".format(name), 'r') as f:
				codec = QTextCodec.codecForName("UTF-8")
				self.setText(codec.toUnicode(f.read()))
		except:
			self.setText(u"TODO")
		
		self.setFont(self.font)
		self.setTabWidth(4)
		self.update_lexer(name)
	
	def update_lexer(self, name, lex=None):
		if not lex:
			lexers, other = load_lexer.load(["dev-theme/dev_lexers", "custom_lexers"])
			lexer = lexers[name]()
		else: lexer = lex
		api = QsciAPIs(lexer)
		regex = re.compile(r"([a-zA-Z0-9#_]{5,})[.]*", re.MULTILINE)
		for mot in regex.findall(str(self.text())):
			api.add(mot)
		api.prepare()
		self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
		self.setAutoCompletionThreshold(1)
		lexer.setFont(self.font)
		self.setLexer(lexer)
		fontmetrics = QFontMetrics(self.font)
		self.setMarginsFont(self.font)
		self.setMarginLineNumbers(1, True)
		self.setMarginWidth(1, fontmetrics.width("00000"))
		self.setMarginsBackgroundColor(QColor("#242424"))
		self.setMarginsForegroundColor(QColor("#999999"))
		return self.lexer()

class HighlightManagerDialog(QDialog):
	""" Manage syntaxe highligting """
	def __init__ (self, parent=None):
		super(HighlightManagerDialog, self).__init__(parent)
		
		Vlayout = QVBoxLayout(self)
		# select language
		select_layout = QHBoxLayout(self)
		select_language = QLabel(u"Selection du langage")
		select_layout.addWidget(select_language)
		self.language = QComboBox(self)
		select_layout.addWidget(self.language)
		select_layout.addStretch(1)
		# color layout
		color_layout = QVBoxLayout(self)
		self.select_enum = QComboBox(self)
		self.color_button = QPushButton(self)
		self.color_button.setObjectName("color_button")
		self.color_button.setFocusPolicy(Qt.NoFocus)
		bg_layout = QHBoxLayout(self)
		self.bg_button = QPushButton(self)
		self.bg_button.setObjectName("bg_button")
		self.bg_button.setFocusPolicy(Qt.NoFocus)
		self.bg_label = QLabel(u"Background-color:\n", self)
		bg_layout.addWidget(self.bg_button)
		bg_layout.addWidget(self.bg_label)
		self.bg_color_button = QColor(0,0,0)
		
		self.color_label = QLabel(self)
		save_label = QLabel(u"/!\\ ATTENTION, penser à enregistrer les modifications\n avant de changer de langage.", self)
		save_label.setStyleSheet("color: rgb(200,0,0);")
		self.save_button = QPushButton(u"Enregistrer")
		color_label_layout = QHBoxLayout(self)
		color_label_layout.addWidget(self.color_button)
		color_label_layout.addWidget(self.color_label)
		color_layout.addWidget(self.select_enum)
		color_layout.addLayout(color_label_layout)
		color_layout.addStretch(1)
		color_layout.addLayout(bg_layout)
		color_layout.addStretch(1)
		color_layout.addWidget(save_label)
		color_layout.addWidget(self.save_button)
		# sample
		self.sample = Sample()
		# color_sample_layout
		color_sample = QHBoxLayout(self)
		color_sample.addLayout(color_layout)
		color_sample.addWidget(self.sample)
		# quit
		quit_button = QPushButton("Quitter")
		quit_button.clicked.connect(self.accept)
		quit_layout = QHBoxLayout(self)
		quit_layout.addStretch(1)
		quit_layout.addWidget(quit_button)
		Vlayout.addLayout(select_layout)
		Vlayout.addLayout(color_sample)
		Vlayout.addLayout(quit_layout)
		self.setLayout(Vlayout)
		# connect
		self.color_button.clicked.connect(self.color_choice)
		self.bg_button.clicked.connect(self.bg_choice)
		self.language.currentIndexChanged[str].connect(self.lang_changed)
		self.select_enum.currentIndexChanged[str].connect(self.enum_changed)
		self.save_button.clicked.connect(self.save)
		# retrieve all langages with qscilexer
		self.lexers = load_lexer.load(["dev-theme/dev_lexers", "custom_lexers"])[0]
		for name in self.lexers:
			self.language.addItem(name)
		# action
		quitter = QAction("Quitter", self)
		quitter.setShortcut("ctrl+Q")
		quitter.triggered.connect(self.accept)
		self.addAction(quitter)
		# resize window
		screen = QDesktopWidget().availableGeometry()
		coef = 0.6
		self.resize(screen.width()*coef, screen.height()*coef)
		size =  self.geometry()
		self.setGeometry((screen.width() - size.width())/2, (screen.height() - size.height())/2, size.width(), size.height())
	
	def bg_choice(self):
		color = QColorDialog.getColor(self.current_lexer.defaultPaper(0))
		self.bg_button.setStyleSheet("background-color: {0};".format(color.name()))
		self.bg_label.setText(u"Background-color:\nrgb({0}, {1}, {2})".format(*self.current_lexer.defaultPaper(0).getRgb()))
		self.current_lexer.setPaper(color)
		self.current_lexer.setDefaultPaper(color)
		self.sample.update_lexer(str(self.language.currentText()), self.current_lexer)
	
	def color_choice(self):
		color = QColorDialog.getColor(self.bg_color_button)
		if color.isValid():
			self.color_button.setStyleSheet("background-color: {0};".format(color.name()))
			self.color_label.setText(u"rgb({0}, {1}, {2})".format(*color.getRgb()))
			items = self.items_from_Qsci(str(self.language.currentText()))
			self.current_lexer.setColor(color, items[str(self.select_enum.currentText())])
			self.sample.update_lexer(str(self.language.currentText()), self.current_lexer)
	
	def enum_changed(self, name):
		if not name.isEmpty():
			items = self.items_from_Qsci(str(self.language.currentText()))
			self.bg_color_button = self.current_lexer.color(items[str(name)])
			self.color_button.setStyleSheet("background-color: {0};".format(self.bg_color_button.name()))
			self.color_label.setText(u"rgb({0}, {1}, {2})".format(*self.bg_color_button.getRgb()))
	
	def lang_changed(self, name):
		self.sample.open_sample(str(name))
		self.current_lexer = self.sample.update_lexer(str(name))
		self.bg_button.setStyleSheet("background-color: {0};".format(self.current_lexer.defaultPaper(0).name()))
		self.bg_label.setText(u"Background-color:\nrgb({0}, {1}, {2})".format(*self.current_lexer.defaultPaper(0).getRgb()))
		self.select_enum.clear()
		for item in self.items_from_Qsci(str(name)):
			self.select_enum.addItem(item)
	
	def items_from_Qsci(self, name):
		if name in ["JavaScript", "Java", "CSharp", "IDL"]:
			lexer = "CPP"
		elif name == "XML":
			lexer = "HTML"
		elif name == "Fortran":
			lexer = "Fortran77"
		elif name == "Octave":
			lexer = "Matlab"
		else:
			lexer = name
		module = __import__("PyQt4.Qsci")
		class_dict = module.Qsci.__dict__["QsciLexer{0}".format(lexer)].__dict__
		return {elt: val for elt, val in class_dict.items() if type(val) == int}
	
	def save(self):
		lang = str(self.language.currentText())
		with open("dev-theme/dev_lexers/dev_{0}.py".format(lang.lower()), 'w') as f:
			f.write("""#!/usr/bin/env python
#-*- coding:utf-8 -*-
from PyQt4.QtGui import QColor, QFont
from PyQt4.Qsci import QsciLexer{0}
class Dev_{1}(QsciLexer{0}):
	def __init__(self, *args):
		super(Dev_{1}, self).__init__(*args)""".format(lang, lang.lower()))
			for item, val in self.items_from_Qsci(lang).items():
				f.write("""
		self.setColor(QColor({2},{3},{4}), QsciLexer{0}.{1})""".format(lang, item, *self.current_lexer.color(val).getRgb()))
			f.write("""
		self.setPaper(QColor({0},{1},{2}))
		self.setDefaultPaper(QColor({0},{1},{2}))
		""".format(*self.current_lexer.defaultPaper(0).getRgb()))
			

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	with open("dev-theme/dev_theme.css") as t:
		dev_theme = t.read()
	app.setStyleSheet(dev_theme)
	dialog = HighlightManagerDialog()
	dialog.show()
	sys.exit(app.exec_())

	#~ def keywords(self, ens):
		#~ if ens == 1:
			#~ return "and as assert break class continue def del elif else except exec finally for from global if import in is lambda None True False not or pass print raise return try while with yield"
		#~ elif ens == 2:
			#~ return "self abs divmod input open staticmethod all enumerate int ord str any eval isinstance pow sum basestring execfile issubclass super bin file iter property tuple bool filter len range type bytearray float list raw_input unichr callable format locals reduce unicode chr frozenset long reload vars classmethod getattr map repr xrange cmp globals max reversed zip compile hasattr memoryview round __import__ complex hash min set apply delattr help next setattr buffer dict hex object slice coerce dir id oct sorted intern"

