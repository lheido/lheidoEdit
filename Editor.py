#!/usr/bin/env python
#-*- coding:utf-8 -*-
import re
from os import listdir
from os.path import basename, getmtime, abspath, exists
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import QsciScintilla, QsciAPIs, QsciCommand
from extend import extend_manager
import load_lexer

@extend_manager(mth=False)
class Editor(QsciScintilla):
	""" Editor based on QsciScintilla """
	
	def __init__ (self, f_path="", parent=None):
		super(Editor, self).__init__()
		self.parent = parent
		self.setUtf8(True)
		self.file_path = str(f_path)
		self.basename = basename(self.file_path)
		#~ self.settings = QSettings("lheidoEdit.conf", QSettings.IniFormat)
		self.language_extension = {
			"Python": ["py"], "CPP": ["c","cpp","h"], "HTML": ["html","php"], "CSS": ["css"],
			"Ruby": ["rb"], "SQL": ["sql"], "Perl": ["pl","pm","perl","agi","pod"], "JavaScript": ["js"],
			"Lua": ["lua"], "Bash": ["sh","zsh","tcsh","ksh","ash","configure"], "D": ["d","di"],
			"Java": ["java","jsp"], "Makefile": ["makefile","MakeFile","Makefile","mk","mak","GNUmakefile"],
			"TCL": ["tcl","tk","wish"], "VHDL": ["vhd","vhdl"], "Verilog": ["v"],
			"XML": ["xml","sgml","xsl","xslt","xsd","xhtml"], "YAML": ["yaml","yml"],
			"Diff": ["diff","patch","rej"], "TeX": ["tex","sty","idx","ltx","latex"], 
			"CMake": ["cmake","ctest"], "Matlab": ["m"]
		}
		
		self.lexers, new_langage = load_lexer.load(["dev-theme/dev_lexers", "custom_lexers"])
		for elt in new_langage:
			self.language_extension[elt] = new_langage[elt] 
		if self.file_path != "":
			self.open_file()
		else:
			self.new_file()
		self.modificationChanged[bool].connect(self.modifChanged)
		#~ self.menu = self.createStandardContextMenu()
		#~ action = self.menu.addAction(u"Delete line", self, SLOT(self.delete_line()))
		#~ stdCmd = self.standardCommands()
		#~ cmd = stdCmd.find(QsciCommand.LineDelete)
		#~ if cmd and cmd.key():
			#~ action.setShortcut(QKeySequence(cmd.key()))
		#~ action.setEnabled(False)
	#~ 
	#~ def delete_line(self):
		#~ self.SendScintilla(QsciScintilla.SCI_LINEDELETE, 0, 0)
		#~ pass
	
	def modifChanged(self, m):
		self.parent.modifChanged(m)
	
	def get_name (self):
		return self.basename
	
	def get_path (self):
		return self.file_path
	
	#~ def _lexer(self):
		#~ default_lexer_module = __import__("PyQt4.Qsci")
		#~ regex = re.compile(r"(?<=QsciLexer)(.+)")
		#~ default_lexers = {}
		#~ for name, lexer in default_lexer_module.Qsci.__dict__.items():
			#~ r = regex.search(name)
			#~ if r and "Custom" not in name:
				#~ default_lexers[r.group(0)] = lexer()
		#~ 
		#~ path = abspath("dev-theme/dev_lexers")
		#~ if exists(path):
			#~ sys.path.append(path)
			#~ regex2 = re.compile(r"(^.+)\.py$")
			#~ lexers_list = [regex2.sub(r"\1", elt) for elt in listdir(path) if regex2.search(elt)]
			#~ for elt in lexers_list:
				#~ tmp = __import__(elt)
				#~ tmp = reload(tmp)
				#~ cl = tmp.__dict__[elt.capitalize()]
				#~ name = regex.search(cl.__bases__[0].__name__)
				#~ name = name.group(0)
				#~ if name not in default_lexers:
					#~ name = cl.__name__
					#~ self.language_extension[name] = [name.lower()]
				#~ default_lexers[name] = cl()
		#~ path = abspath("custom_lexers")
		#~ if exists(path):
			#~ sys.path.append(path)
			#~ regex2 = re.compile(r"(^.+)\.py$")
			#~ lexers_list = [regex2.sub(r"\1", elt) for elt in listdir(path) if regex2.search(elt)]
			#~ for elt in lexers_list:
				#~ tmp = __import__(elt)
				#~ tmp = reload(tmp)
				#~ cl = tmp.__dict__[elt.capitalize()]
				#~ name = regex.search(cl.__bases__[0].__name__)
				#~ name = name.group(0)
				#~ if name not in default_lexers:
					#~ name = cl.__name__
					#~ self.language_extension[name] = [name.lower()]
				#~ default_lexers[name] = cl()
		#~ return default_lexers
	
	def _lang(self):
		extension = re.sub(r'.+\.(.+)$', r'\1', self.basename)
		for key, value in self.language_extension.items():
			if extension in value:
				return key
		return ""
	
	def __save (self):
		with open(self.file_path, "w") as f:
			f.write(self.get_text())
		self.update_config()
		self.setModified(False)
	
	@extend_manager()
	def save_as (self):
		self.file_path = str(QFileDialog.getSaveFileName(self, "Enregistrer le fichier", "."))
		if self.file_path != "":
			self.basename = basename(self.file_path)
			self.__save()
	
	@extend_manager()
	def save_file (self):
		if self.file_path == "":
			self.save_as()
		else:
			self.__save()
	
	def get_text (self):
		codec = QTextCodec.codecForName("UTF-8")
		return str(codec.fromUnicode(self.text()))
	
	def set_text (self, text):
		codec = QTextCodec.codecForName("UTF-8")
		self.setText(codec.toUnicode(text))
	
	@extend_manager()
	def open_file (self):
		with open(self.file_path, "r") as f:
			fichier = f.read()
		self.set_text(fichier)
		self.update_config()
		self.setModified(False)
	
	@extend_manager()
	def new_file (self):
		self.basename = "Nouveau fichier"
		self.update_config()
		self.setModified(False)
		
	def update_config(self):
		# Set the default font
		settings = QSettings("lheido", "lheidoEdit")
		font = QFont()
		font.setFamily('Ubuntu Mono')
		font.setFixedPitch(True)
		font.setPointSize(12)
		self.setFont(font)
		self.lexers, new_langage = load_lexer.load(["dev-theme/dev_lexers", "custom_lexers"])
		self.lang = self._lang()
		try:
			self.date = getmtime(self.file_path)
		except Exception, ex:
			self.date = -1
		try:
			lexer = self.lexers[self.lang]()
			lexer.setFont(font)
			self.__auto_completion(lexer)
			self.setLexer(lexer)
		except Exception, ex:
			print "erreur lexer update", ex
			self.setPaper(QColor(33,33,33))
			self.setColor(QColor("#FFFFFF"))
		# Margin 1 is used for line numbers
		fontmetrics = QFontMetrics(font)
		self.setMarginsFont(font)
		self.setMarginLineNumbers(1, True)
		self.setMarginWidth(1, fontmetrics.width("00000"))
		self.setMarginsBackgroundColor(QColor("#242424"))
		self.setMarginsForegroundColor(QColor("#999999"))
		self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
		# Current line visible with special background color
		self.setCaretLineVisible(True)
		self.setCaretLineBackgroundColor(QColor(23, 23, 23))
		self.setCaretForegroundColor(QColor("#FFFFFF"))
		self.setIndentationGuides(True)
		self.setIndentationGuidesForegroundColor(QColor(23,23,23))
		if settings.value("editeur/indent_type").toInt() == 1:
			self.setIndentationsUseTabs(True)
		self.setTabWidth(settings.value("editeur/indent_width", QVariant(4)).toInt()[0])
		self.setAutoIndent(True)
		self.setAutoCompletionThreshold(4)
		self.setAutoCompletionSource(QsciScintilla.AcsAPIs)
		if settings.value("editeur/pliage", QVariant(True)).toBool():
			self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
			self.setFoldMarginColors(QColor("#242424"), QColor("#242424"))
		self.update()
	
	def __auto_completion(self, lexer):
		api = QsciAPIs(lexer)
		regex = re.compile(r"([a-zA-Z0-9#_]{5,})[.]*", re.MULTILINE)
		for mot in regex.findall(self.get_text()):
			api.add(mot)
		api.prepare()
