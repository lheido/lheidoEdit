#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Editor import Editor
from GpTab import GpTab
from settingsDialog import SettingsDialog
from highlightManagerDialog import HighlightManagerDialog
from extend import extend_manager

class Splitter(QSplitter):
	def __init__ (self, align):
		super(Splitter, self).__init__(align)
	
	def update_splitter_id(self):
		count = self.count()
		for i in xrange(count):
			self.widget(i).splitter_id = i
	
	def remove_splitter_widget(self, supp_id):
		split = self.widget(supp_id)
		split.hide()
		split.setParent(None)
		del split
		self.update_splitter_id()
		if self.count() > 0:
			self.widget(self.count()-1).setFocus(True)

@extend_manager(mth=False)
class MainLayout(QWidget):
	""" main Layout """
	
	def __init__ (self, parent=None):
		super(MainLayout, self).__init__(parent)
		self.action_manager = {"new_action": parent._new_action, "new_menu": parent._new_menu}
		self.Hbox = QHBoxLayout(parent)
		self.splitter = Splitter(Qt.Horizontal)
		settings = QSettings("lheido", "lheidoEdit")
		if settings.value("general/prec_session", QVariant(False)).toBool():
			self.read_opened_files()
		else:
			self._add_splitter(True, None)
		self.Hbox.addWidget(self.splitter)
		self.splitter.setFocusPolicy(Qt.NoFocus)
		self.splitter.setFocusProxy(self.splitter.widget(0))
		self.setLayout(self.Hbox)
		self.actions(parent=parent)
	
	@extend_manager()
	def actions(self, **kwargs):
		""" actions(parent=parent) """
		kwargs["parent"]._new_action(name="&Diviser", shortcut="ctrl+b", fun=self.add_splitter, menu="Affichage")
		kwargs["parent"]._new_action(name="&Nouveau fichier", shortcut="ctrl+n", fun=self.__new_file, menu="Fichier")
		kwargs["parent"]._new_action(name="&Ouvrir un fichier", shortcut="ctrl+o", fun=self.__open_file, menu="Fichier")
		kwargs["parent"]._new_action(name="&Toggle Focus", shortcut="alt+w", fun=self.toggle_focus, menu="Affichage")
		kwargs["parent"]._new_action(name="&Next tab", shortcut="alt+<", fun=self._next_tab, menu="Affichage")
		kwargs["parent"]._new_action(name="&Prev tab", shortcut="alt+shift+<", fun=self._prev_tab, menu="Affichage")
		kwargs["parent"]._new_action(name=u"&Déplacer onglet vers le groupe suivante", shortcut="ctrl+shift+b", fun=self.move_tab_to_right, menu="Affichage")
		kwargs["parent"]._new_action(name=u"&Déplacer onglet vers le groupe précédent", shortcut="ctrl+alt+b", fun=self.move_tab_to_left, menu="Affichage")
		kwargs["parent"]._new_action(name="&Enregistrer", shortcut="ctrl+s", fun=self.__save_file, menu="Fichier")
		kwargs["parent"]._new_action(name="Enregistrer &sous", shortcut="ctrl+shift+s", fun=self.__save_as, menu="Fichier")
		kwargs["parent"]._new_action(name="&Fermer l'onglet courant", shortcut="ctrl+w", fun=self._remove_tab, menu="Fichier")
		kwargs["parent"]._new_action(name="&Fermer le groupe d'onglet courant", shortcut="ctrl+shift+w", fun=self._remove_group, menu="Fichier")
		kwargs["parent"]._new_action(name="Print Focus", shortcut="ctrl+alt+w", fun=self.__get_focus, menu="Fichier")
	
	@extend_manager()
	def add_splitter (self):
		self._add_splitter(True)
	
	def _add_splitter (self, new=False, widget=None):
		count = self.splitter.count()
		self.splitter.addWidget(GpTab(count, new, widget, self.splitter))
		self.setFocusProxy(self.splitter.widget(count))
		self.splitter.widget(count).setFocus(True)
	
	@extend_manager()
	def hide_splitter (self):
		pass
	
	@extend_manager()
	def _remove_tab (self):
		cur_id_splitter = self._retrieve_focus()
		cur_tab = self.splitter.widget(cur_id_splitter).currentIndex()
		self.splitter.widget(cur_id_splitter).tabCloseRequested.emit(cur_tab)
	
	@extend_manager()
	def _remove_group (self):
		cur_id_splitter = self._retrieve_focus()
		self.splitter.widget(cur_id_splitter).remove_all()
	
	@extend_manager()
	def move_tab_to_right (self):
		cur_id = self._retrieve_focus()
		nb_group = self.splitter.count()
		if nb_group > 1:
			if nb_group != cur_id + 1:
				gp = self.splitter.widget(cur_id)
				if gp.count() > 1:
					new_id = cur_id + 1
				else:
					new_id = cur_id
				widget = gp.get_tab()
				self.splitter.widget(new_id).add_tab(widget)
		else:
			gp = self.splitter.widget(cur_id)
			widget = gp.get_tab()
			self._add_splitter(False, widget)
	
	@extend_manager()
	def move_tab_to_left (self):
		cur_id = self._retrieve_focus()
		nb_group = self.splitter.count()
		if nb_group > 1:
			if cur_id - 1 >= 0:
				widget = self.splitter.widget(cur_id).get_tab()
				self.splitter.widget(cur_id - 1).add_tab(widget)
		
	def toggle_focus (self):
		count = self.splitter.count()
		cur_id = self._retrieve_focus()
		new_id = cur_id + 1
		if new_id == count: new_id = 0
		self.splitter.setFocusProxy(self.splitter.widget(new_id))
		self.splitter.widget(new_id).setFocus(True)
		return new_id
	
	def read_opened_files(self):
		settings = QSettings("lheido", "lheidoEdit")
		size = settings.beginReadArray("opened_files")
		for i in xrange(size):
			settings.setArrayIndex(i)
			files_path = str(settings.value("files_path").toString())
			files_path = files_path.split(";")
			widgets = [Editor(files, self) for files in files_path]
			self._add_splitter(False, widgets[0])
			for other in widgets[1:]:
				self.splitter.widget(i).add_tab(other)
		settings.endArray()
	
	def _set_opened_files(self):
		settings = QSettings("lheido", "lheidoEdit")
		settings.beginWriteArray("opened_files")
		for i in xrange(self.splitter.count()):
			settings.setArrayIndex(i)
			settings.setValue("files_path", self.splitter.widget(i).get_opened_files())
		settings.endArray()
		settings.sync()
	
	def _quit(self):
		for i in xrange(self.splitter.count()):
			self.splitter.widget(i).check_modified()
		self._set_opened_files()
	
	def __get_focus (self):
		print self.splitter.count()
		#~ print QApplication.focusWidget()
		#~ for i in range(self.splitter.count()):
			#~ print i
			#~ widget = self.splitter.widget(i)
			#~ for j in range(widget.count()):
				#~ print "  ", j, "{0}".format(widget.widget(j).hasFocus() and "has focus" or "no focus")
	
	def _retrieve_focus(self):
		for i in range(self.splitter.count()):
			if self.splitter.widget(i).hasFocus():
				return i
	
	@extend_manager()
	def __new_file(self):
		if self._retrieve_focus() >= 0: # cas ou un splitter.widget a le focus
			self.splitter.widget(self._retrieve_focus())._new_file()
		else: # cas ou il n'y a plus de widgets GpTab
			self._add_splitter(True)
	
	@extend_manager()
	def __open_file(self):
		if self._retrieve_focus() >= 0:
			self.splitter.widget(self._retrieve_focus())._open_file()
		else:
			self._add_splitter()
	
	@extend_manager()
	def _next_tab(self):
		self.splitter.widget(self._retrieve_focus()).switch_tab(True)
	
	@extend_manager()
	def _prev_tab(self):
		self.splitter.widget(self._retrieve_focus()).switch_tab(False)
	
	@extend_manager()
	def __save_file(self):
		self.splitter.widget(self._retrieve_focus())._save_file()
	
	@extend_manager()
	def __save_as(self):
		self.splitter.widget(self._retrieve_focus())._save_as()
	
	def _clear_focus(self):
		for i in range(self.splitter.count()):
			self.splitter.widget(i)._clear_focus()

@extend_manager(mth=False)	
class MainWindow(QMainWindow):
	""" Main window for lheidoEdit """
	
	def __init__ (self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.statusbar = self.statusBar()
		self.setWindowTitle("LheidoEdit")
		self.menubar = self.menuBar()
		self.menus = {
			"Fichier": self.menubar.addMenu("&Fichier"),
			"Affichage": self.menubar.addMenu("&Affichage"),
			"Outils": self.menubar.addMenu("&Outils")
		}
		# add action exit and toggle menubar to mainWindow
		self.mainLayout = MainLayout(self)
		self.setCentralWidget(self.mainLayout)
		self._new_action(name="&Quitter", shortcut="ctrl+q", fun=self.__quit, menu="Fichier")
		self._new_action(name="&Afficher/cacher la bar de menu", shortcut="ctrl+F1", fun=self._toggle_menu_bar, menu="Affichage")
		self._new_action(name="&HighlightManager", shortcut="ctrl+F2", fun=self.highlight_manager, menu="Outils")
		self._new_action(name="&Préférences", shortcut="ctrl+alt+p", fun=self.settings)
		self.__window_button()
		settings = QSettings("lheido", "lheidoEdit")
		if settings.value("mainwindow/maximized", QVariant(False)).toBool():
			self.showMaximized()
		else:
			self.resize(settings.value("mainwindow/size", QSize(400, 400)).toSize())
			self.move(settings.value("mainwindow/pos", QPoint(0,0)).toPoint())
	
	def __quit(self):
		self.mainLayout._quit()
		settings = QSettings("lheido", "lheidoEdit")
		if settings.value("general/save_geo", QVariant(True)).toBool():
			settings.setValue("mainwindow/size", self.size())
			settings.setValue("mainwindow/maximized", self.isMaximized())
			settings.setValue("mainwindow/pos", self.pos())
			settings.sync()
		self.close()
	
	def highlight_manager(self):
		dialog = HighlightManagerDialog(self)
		dialog.show()
	
	@extend_manager()
	def _toggle_menu_bar(self):
		self.menubar.setVisible(not self.menubar.isVisible())
	
	@extend_manager()
	def _new_action(self, **kwargs):
		""" _new_action(name=, shortcut=, fun=, menu=None) """
		action = QAction(kwargs["name"], self)
		action.setShortcut(kwargs["shortcut"])
		action.triggered.connect(kwargs["fun"])
		self.addAction(action)
		if "menu" in kwargs:
			self.menus[kwargs["menu"]].addAction(action)
	
	@extend_manager()
	def _new_menu(self, **kwargs):
		""" _new_menu(name=) """
		if kwargs["name"] not in self.menus:
			self.menus[kwargs["name"]] = self.menubar.addMenu("&{0}".format(kwargs["name"]))
	
	def __window_button(self):
		widget = QWidget(self)
		layout = QHBoxLayout(self)
		layout.setSpacing(0)
		close = QPushButton("")
		close.setObjectName("alternate_close")
		close.clicked.connect(self.__quit)
		close.setFocusPolicy(Qt.NoFocus)
		close.setToolTip(u"Fermer")
		mini = QPushButton("")
		mini.setObjectName("alternate_mini")
		mini.setToolTip(u"Minimiser")
		mini.clicked.connect(self.showMinimized)
		mini.setFocusPolicy(Qt.NoFocus)
		maxi = QPushButton("")
		maxi.setObjectName("alternate_maxi")
		maxi.setToolTip(u"Maximiser")
		maxi.setCheckable(True)
		maxi.clicked[bool].connect(self.toggleMaximized)
		maxi.setFocusPolicy(Qt.NoFocus)
		layout.addWidget(close)
		layout.addWidget(mini)
		layout.addWidget(maxi)
		layout.addStretch(1)
		widget.setLayout(layout)
		pref = QPushButton(u"")
		pref.setObjectName("settings")
		pref.setIcon(QIcon(".imgs/settings.png"))
		pref.setIconSize(QSize(15,14))
		pref.setToolTip(u"Préférences")
		pref.clicked.connect(self.settings)
		pref.setFocusPolicy(Qt.NoFocus)
		self.menubar.setCornerWidget(widget, Qt.TopLeftCorner)
		self.menubar.setCornerWidget(pref, Qt.TopRightCorner)
		#~ self.menubar.mousePressEvent = self.__mousePressEvent
		#~ self.menubar.mouseMoveEvent = self.__mouseMoveEvent
	
	def settings(self):
		settings = SettingsDialog(self)
		if settings.exec_():
			print settings.get_settings()
		else:
			settings.get_error()
	
	def toggleMaximized(self, pressed):
		if pressed: self.showMaximized()
		else: self.showNormal()
	
	#~ def mousePressEvent(self, event):
	    #~ self.offset = event.pos()
	#~ 
	#~ def mouseMoveEvent(self, event):
	    #~ x=event.globalX()
	    #~ y=event.globalY()
	    #~ x_w = self.offset.x()
	    #~ y_w = self.offset.y()
	    #~ self.move(x-x_w, y-y_w)

