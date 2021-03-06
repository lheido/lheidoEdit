#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from os.path import exists
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
		settings = QSettings("lheido", "lheidoEdit")
		kwargs["parent"]._new_action(identifier="NewGp", name=u"&Nouveau groupe", shortcut=settings.value("shortcut/NewGp").toString(), fun=self.add_splitter, menu="Affichage")
		kwargs["parent"]._new_action(identifier="NewFile", name=u"&Nouveau fichier", shortcut=settings.value("shortcut/NewFile").toString(), fun=self.__new_file, menu="Fichier")
		kwargs["parent"]._new_action(identifier="Open", name=u"&Ouvrir un fichier", shortcut=settings.value("shortcut/Open").toString(), fun=self.__open_file, menu="Fichier")
		kwargs["parent"]._new_action(identifier="OpenNewGp", name=u"Ouvrir un fichier dans un nouveau groupe", shortcut=settings.value("shortcut/OpenNewGp").toString(), fun=self.__open_new_splitter, menu="Fichier")
		kwargs["parent"]._new_action(identifier="ChangeGp", name=u"&Toggle Focus", shortcut=settings.value("shortcut/ChangeGp").toString(), fun=self.toggle_focus, menu="Affichage")
		kwargs["parent"]._new_action(identifier="NextTab", name=u"&Next tab", shortcut=settings.value("shortcut/NextTab").toString(), fun=self._next_tab, menu="Affichage")
		kwargs["parent"]._new_action(identifier="PrevTab", name=u"&Prev tab", shortcut=settings.value("shortcut/PrevTab").toString(), fun=self._prev_tab, menu="Affichage")
		kwargs["parent"]._new_action(identifier="TabNextGp", name=u"&Déplacer onglet vers le groupe suivante", shortcut=settings.value("shortcut/TabNextGp").toString(), fun=self.move_tab_to_right, menu="Affichage")
		kwargs["parent"]._new_action(identifier="TabPrevGp", name=u"Déplacer onglet vers le groupe précédent", shortcut=settings.value("shortcut/TabPrevGp").toString(), fun=self.move_tab_to_left, menu="Affichage")
		kwargs["parent"]._new_action(identifier="Save", name=u"&Enregistrer", shortcut=settings.value("shortcut/Save").toString(), fun=self.__save_file, menu="Fichier")
		kwargs["parent"]._new_action(identifier="SaveAs", name=u"Enregistrer &sous", shortcut=settings.value("shortcut/SaveAs").toString(), fun=self.__save_as, menu="Fichier")
		kwargs["parent"]._new_action(identifier="CloseTab", name=u"&Fermer l'onglet courant", shortcut=settings.value("shortcut/CloseTab").toString(), fun=self._remove_tab, menu="Fichier")
		kwargs["parent"]._new_action(identifier="CloseGp", name=u"Fermer le groupe d'onglet courant", shortcut=settings.value("shortcut/CloseGp").toString(), fun=self._remove_group, menu="Fichier")
		kwargs["parent"]._new_action(identifier="Execute", name=u"Exécuter", shortcut=settings.value("shortcut/Execute").toString(), fun=self._execute, menu="Outils")
		#~ kwargs["parent"]._new_action(name="Print Focus", shortcut="ctrl+alt+w", fun=self.__get_focus, menu="Fichier")
	
	def _execute(self):
		grp = self.splitter.widget(self._retrieve_focus())
		grp._execute()
	
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
			widgets = [Editor(files, self) for files in files_path if exists(files)]
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
	
	def __open_new_splitter(self):
		self._add_splitter(False, None)
	
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
	
	def _update(self):
		for i in xrange(self.splitter.count()):
			self.splitter.widget(i)._update()

class MenuBar(QMenuBar):
	
	def __init__ (self, parent=None):
		super(MenuBar, self).__init__(parent)
		self.parent = parent
		self.offset = None
		self.menus = {
			"Fichier": self.addMenu("&Fichier"),
			"Affichage": self.addMenu("&Affichage"),
			"Outils": self.addMenu("&Outils")
		}
		widget = QWidget(self)
		layout = QHBoxLayout(self)
		layout.setSpacing(0)
		self.close_button = QPushButton("")
		self.close_button.setObjectName("alternate_close")
		self.close_button.setFocusPolicy(Qt.NoFocus)
		self.close_button.setToolTip(u"Fermer")
		self.mini_button = QPushButton("")
		self.mini_button.setObjectName("alternate_mini")
		self.mini_button.setToolTip(u"Minimiser")
		self.mini_button.setFocusPolicy(Qt.NoFocus)
		self.maxi_button = QPushButton("")
		self.maxi_button.setObjectName("alternate_maxi")
		self.maxi_button.setToolTip(u"Maximiser")
		self.maxi_button.setCheckable(True)
		self.maxi_button.setFocusPolicy(Qt.NoFocus)
		layout.addWidget(self.close_button)
		layout.addWidget(self.mini_button)
		layout.addWidget(self.maxi_button)
		layout.addStretch(1)
		widget.setLayout(layout)
		self.pref_button = QPushButton(u"")
		self.pref_button.setObjectName("settings")
		self.pref_button.setIcon(QIcon(".imgs/settings.png"))
		self.pref_button.setIconSize(QSize(15,14))
		self.pref_button.setToolTip(u"Préférences")
		self.pref_button.setFocusPolicy(Qt.NoFocus)
		self.setCornerWidget(widget, Qt.TopLeftCorner)
		self.setCornerWidget(self.pref_button, Qt.TopRightCorner)
	
	def mousePressEvent(self, event):
		if event.button() == Qt.RightButton:
			self.offset = event.pos()
		super(MenuBar, self).mousePressEvent(event)
	
	def mouseReleaseEvent(self, event):
		self.offset = None
		super(MenuBar, self).mouseReleaseEvent(event)
	
	def mouseMoveEvent(self, event):
		x=event.globalX()
		y=event.globalY()
		if self.offset:
			x_w = self.offset.x()
			y_w = self.offset.y()
			self.parent.move(x-x_w, y-y_w)
		super(MenuBar, self).mouseMoveEvent(event)

@extend_manager(mth=False)	
class MainWindow(QMainWindow):
	""" Main window for lheidoEdit """
	
	def __init__ (self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.statusbar = self.statusBar()
		self.setWindowTitle("LheidoEdit")
		#~ self.menubar = self.menuBar()
		self.menubar = MenuBar(self)
		self.setMenuBar(self.menubar)
		self._actions = {}
		settings = QSettings("lheido", "lheidoEdit")
		# add action exit and toggle menubar to mainWindow
		self.mainLayout = MainLayout(self)
		self.setCentralWidget(self.mainLayout)
		self._new_action(identifier="Quit", name=u"&Quitter", shortcut=settings.value("shortcut/Quit").toString(), fun=self.__quit, menu="Fichier")
		self._new_action(identifier="ToggleMenuBar", name=u"&Afficher/cacher la barre de menu", shortcut=settings.value("shortcut/ToggleMenuBar").toString(), fun=self._toggle_menu_bar, menu="Affichage")
		self._new_action(identifier="HighLightM", name=u"&HighlightManager", shortcut=settings.value("shortcut/HighLightM").toString(), fun=self.highlight_manager, menu="Outils")
		self._new_action(identifier="UserPref", name=u"&Préférences", shortcut=settings.value("shortcut/UserPref").toString(), fun=self.settings)
		self.__menubar_event()
		if settings.value("mainwindow/maximized", QVariant(False)).toBool():
			self.showMaximized()
		else:
			self.resize(settings.value("mainwindow/size", QSize(400, 400)).toSize())
			self.move(settings.value("mainwindow/pos", QPoint(0,0)).toPoint())
		if settings.value("mainwindow/hideMenuBar", QVariant(False)).toBool():
			self.menubar.setVisible(False)
	
	def __quit(self):
		reply = QMessageBox.Yes
		settings = QSettings("lheido", "lheidoEdit")
		if settings.value("general/valide_fermeture", QVariant(False)).toBool():
			msg = u"Voulez vous vraiment quitter l'application?"
			reply = QMessageBox.question(self, u"Confirmation", msg, QMessageBox.Yes, QMessageBox.No)
		if reply == QMessageBox.Yes:
			self.mainLayout._quit()
			if settings.value("general/save_geo", QVariant(True)).toBool():
				settings.setValue("mainwindow/size", self.size())
				settings.setValue("mainwindow/maximized", self.isMaximized())
				settings.setValue("mainwindow/pos", self.pos())
				settings.setValue("mainwindow/hideMenuBar", self.menubar.isHidden())
				settings.sync()
			self.close()
	
	@extend_manager()
	def _toggle_menu_bar(self):
		self.menubar.setVisible(not self.menubar.isVisible())
	
	@extend_manager()
	def _new_action(self, **kwargs):
		""" _new_action(identifier=, name=, shortcut=, fun=, menu=None) """
		action = QAction(kwargs["name"], self)
		action.setShortcut(kwargs["shortcut"])
		action.triggered.connect(kwargs["fun"])
		self.addAction(action)
		self._actions[kwargs["identifier"]] = action
		if "menu" in kwargs:
			self.menubar.menus[kwargs["menu"]].addAction(action)
	
	@extend_manager()
	def _new_menu(self, **kwargs):
		""" _new_menu(name=) """
		if kwargs["name"] not in self.menus:
			self.menubar.menus[kwargs["name"]] = self.menubar.addMenu("&{0}".format(kwargs["name"]))
	
	def __menubar_event(self):
		self.menubar.close_button.clicked.connect(self.__quit)
		self.menubar.mini_button.clicked.connect(self.showMinimized)
		self.menubar.maxi_button.clicked[bool].connect(self.toggleMaximized)
		self.menubar.pref_button.clicked.connect(self.settings)
	
	def settings(self):
		settings = SettingsDialog(self)
		settings.show()
		settings.accepted.connect(self.accepted_activate)
	
	def highlight_manager(self):
		dialog = HighlightManagerDialog(self)
		dialog.show()
		dialog.accepted.connect(self.accepted_activate)
	
	def accepted_activate(self):
		self.raise_()
		self.activateWindow()
		self.mainLayout._update()
		self.update_actions()
	
	def update_actions(self):
		settings = QSettings("lheido", "lheidoEdit")
		for action in self.actions():
			for elt, val in self._actions.items():
				if action == val:
					action.setShortcut(str(settings.value("shortcut/{0}".format(elt)).toString()))
	
	def toggleMaximized(self, pressed):
		if pressed: self.showMaximized()
		else: self.showNormal()
