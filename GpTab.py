#!/usr/bin/env python
#-*- coding:utf-8 -*-

from os.path import basename
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import QsciScintilla
from extend import extend_manager
from Editor import Editor

@extend_manager(mth=False)
class GpTab(QTabWidget):
	""" Class GpTab, manage group tab of lheidoEdit """
	
	def __init__ (self, splitter_id, new=False, tab=None, parent=None):
		super(GpTab, self).__init__(parent)
		self.parent = parent
		self.splitter_id = splitter_id
		self.opened_files = {}
		self.setTabsClosable(True)
		self.setMovable(True)
		self.setUsesScrollButtons(True)
		self.setFocusPolicy(Qt.NoFocus)
		self.currentChanged.connect(self.switch_focus)
		self.tabCloseRequested.connect(self.remove_tab)
		widget = QPushButton("", self)
		widget.clicked.connect(self.remove_all)
		widget.setObjectName("gpTabClose")
		widget.setFocusPolicy(Qt.NoFocus)
		widget.setToolTip("Fermer les onglets de ce groupe")
		self.setCornerWidget(widget, Qt.TopLeftCorner)
		#~ if not dev_theme:
			#~ self.addTab(QWidget(), "retrieve default color")
			#~ self.defaultTabColor = self.tabBar().tabTextColor(0)
			#~ self.removeTab(0)
		#~ else 
		self.defaultTabColor = QColor("#FFFFFF")
		if new: self._new_file()
		elif tab: self.add_tab(tab)
		else: self._open_file()
	
	def add_tab(self, widget):
		widget.parent = self
		i = self.addTab(widget, widget.get_name())
		#~ if self.settings.value("dev_theme"):
		self.tabBar().setTabTextColor(i, widget.isModified() and QColor("#FF0000") or self.defaultTabColor)
		self.setCurrentIndex(i)
	
	def __add_edit(self, file_path=""):
		editor = Editor(file_path, self)
		#on garde le nom des fichiers avec leur chemins pour ne pas ouvrir plusieurs fois le même
		if file_path != "":
			self.opened_files[editor.get_name()] = editor.get_path()
		#Add Tab with Editor
		self.add_tab(editor)
	
	@extend_manager()
	def _open_file(self):
		#QFileDialog
		file_path = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", ".")
		self.__add_edit(file_path)
	
	@extend_manager()
	def _new_file(self):
		self.__add_edit()
	
	@extend_manager()
	def _save_file(self):
		index = self.currentIndex()
		editor = self.widget(index)
		editor.save_file()
		self.setTabText(index, editor.get_name())
	
	@extend_manager()
	def _save_as(self):
		index = self.currentIndex()
		editor = self.widget(index)
		editor.save_as()
		self.setTabText(index, editor.get_name())
	
	def switch_tab(self, sens):
		""" sens = True vers la droite, False vers la gauche """
		count = self.count()
		cur_id = self.currentIndex()
		if sens: new_id = cur_id + 1
		else: new_id = cur_id - 1
		if new_id < 0: new_id = count - 1
		if new_id == count: new_id = 0
		self.setCurrentIndex(new_id)
	
	def switch_focus(self, new_index):
		if new_index != -1:
			self.setFocusProxy(self.widget(new_index))
			self.setFocus(True)
		self.widget(new_index).update_config()
	
	def get_tab(self):
		index = self.currentIndex()
		widget = self.currentWidget()
		self.remove_tab(index, save=False)
		return widget
	
	def switch_add(self, widget):
		i = self.addTab(widget, widget.get_name())
		self.setCurrentIndex(i)
		self.tabBar().setTabTextColor(i, QColor("#FFFFFF"))
	
	def remove_tab(self, index, save=True):
		if self.widget(index).isModified() and save:
			msg = u"Le fichier {0} a été modifié\nVoulez vous enregistrer les changements?".format(self.widget(index).get_name())
			reply = QMessageBox.question(self, u"Fichier modifié", msg, QMessageBox.Yes, QMessageBox.No)
			if reply == QMessageBox.Yes:
				self._save_file()
		if self.count() == 1:
			self.parent.remove_splitter_widget(self.splitter_id)
		else:
			self.removeTab(index)
	
	def remove_all(self):
		index_list = [i for i in xrange(self.count())]
		for i in reversed(index_list):
			self.remove_tab(i)
	
	def check_modified(self):
		for i in xrange(self.count()):
			if self.widget(i).isModified():
				msg = u"Le fichier {0} a été modifié\nVoulez vous enregistrer les changements?".format(self.widget(i).get_name())
				reply = QMessageBox.question(self, u"Fichier modifié", msg, QMessageBox.Yes, QMessageBox.No)
				if reply == QMessageBox.Yes:
					self.widget(i).save_file()
	
	def get_opened_files(self):
		return ";".join([self.widget(i).file_path for i in xrange(self.count())])
	
	def modifChanged(self, m):
		if m: color = QColor("#FF0000")
		else: color = self.defaultTabColor 
		index = self.currentIndex()
		self.tabBar().setTabTextColor(index, color)
	
	def _execute(self):
		widget = self.widget(self.currentIndex())
		widget.execute()
	
