#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import QsciScintilla, QsciCommand

class ShortcutsTable(QTableWidget):
	""" custom widget for manage shortcut """
	def __init__(self, editor=True, parent=None):
		super(ShortcutsTable, self).__init__(parent)
		self.setSortingEnabled(False)
		self.setColumnCount(3)
		header = self.horizontalHeader()
		self.setHorizontalHeaderLabels(["id","Raccourcis","Description"])
		self.setColumnHidden(0, True)
		header.setResizeMode(QHeaderView.Interactive)
		header.setDefaultSectionSize(200)
		self.setAlternatingRowColors(True)
		header.setStretchLastSection(True)
		self.verticalHeader().setVisible(False)
		if editor:
			self.shortcut_editor()
		else:
			self.shortcut_ui()
		self.itemChanged.connect(self.item_changed)
	
	def shortcut_editor(self):
		settings = QSettings("lheido", "lheidoEdit")
		editor = QsciScintilla()
		cmds = editor.standardCommands().commands()
		self.id_key = {}
		for i, cmd in enumerate(cmds):
			self.insertRow(self.rowCount())
			command = str(cmd.command())
			key = settings.value("shortcut/{0}".format(command), QKeySequence(cmd.key()).toString()).toString()
			id_item = QTableWidgetItem()
			id_item.setText(command)
			shortcut_item = QTableWidgetItem()
			shortcut_item.setText(key)
			description_item = QTableWidgetItem()
			description_item.setText(cmd.description())
			description_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled )
			self.setItem(i, 0, id_item)
			self.setItem(i, 1, shortcut_item)
			self.setItem(i, 2, description_item)
			self.id_key[command] = key
	
	def shortcut_ui(self):
		settings = QSettings("lheido", "lheidoEdit")
		description = {
			"Quit":         u"Quitter l'éditeur",
			"Open": 	    u"Ouvrir un fichier dans le groupe courant",
			"OpenNewGp":    u"Ouvrir un fichier dans un nouveau groupe",
			"NewFile":      u"Nouveau fichier dans le groupe courant",
			"Save":         u"Enregistrer le fichier courant",
			"SaveAs":       u"Enregistrer le fichier courant sous",
			"ChangeGp":     u"Donne le focus au groupe suivant",
			"NextTab":      u"Onglet suivant",
			"PrevTab":      u"Onglet précédent",
			"NewGp":        u"Nouveau groupe",
			"TabNextGp":    u"Onglet courant vers groupe suivant",
			"TabPrevGp":   u"Onglet courant vers groupe précédent",
			"CloseTab":     u"Fermer l'onglet courant",
			"CloseGp":      u"Fermer le groupe de l'onglet courant",
			"ToggleMenuBar":u"Afficher/Cacher la barre de menu",
			"UserPref":     u"Préférences utilisateur",
			"HighLightM":   u"Outil d'édition de coloration syntaxique"
		}
		self.id_key = {
			"Quit":         "Ctrl+Q",
			"Open": 	    "Ctrl+O",
			"OpenNewGp":    "Ctrl+Shift+O",
			"NewFile":      "Ctrl+N",
			"Save":         "Ctrl+S",
			"SaveAs":       "Ctrl+Shift+S",
			"ChangeGp":     "Alt+W",
			"NextTab":      "Alt+<",
			"PrevTab":      "Alt+Shift+<",
			"NewGp":        "Ctrl+B",
			"TabNextGp":    "Ctrl+Shift+B",
			"TabPrevGp":    "Ctrl+Alt+B",
			"CloseTab":     "Ctrl+W",
			"CloseGp":      "Ctrl+Shift+W",
			"ToggleMenuBar":"Ctrl+F1",
			"UserPref":     "Ctrl+Alt+P",
			"HighLightM":   "Ctrl+F2" 
		}
		for i, cmd in enumerate(self.id_key):
			self.insertRow(self.rowCount())
			id_item = QTableWidgetItem()
			id_item.setText(cmd)
			key = settings.value("shortcut/{0}".format(cmd), QVariant("{0}".format(self.id_key[cmd]))).toString()
			shortcut_item = QTableWidgetItem()
			shortcut_item.setText(key)
			description_item = QTableWidgetItem()
			description_item.setText(description[cmd])
			description_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled )
			self.setItem(i, 0, id_item)
			self.setItem(i, 1, shortcut_item)
			self.setItem(i, 2, description_item)
	
	def item_changed(self, item):
		row = self.row(item)
		item_id = self.item(row, 0).text()
		self.id_key[item_id] = item.text()
	
	def get_dict(self):
		return self.id_key
	
class SettingsDialog(QDialog):
	""" Manage user settings """
	def __init__ (self, parent=None):
		super(SettingsDialog, self).__init__(parent)
		self.setWindowTitle(u"Préférences")
		quitter = QAction("Quitter", self)
		quitter.setShortcut("ctrl+Q")
		quitter.triggered.connect(self.close)
		self.addAction(quitter)
		self.vlayout = QVBoxLayout(self)
		self.setLayout(self.vlayout)
		self._tabwidget()
		self.hlayout = QHBoxLayout(self)
		valide = QPushButton("Valider")
		valide.clicked.connect(self.accept)
		annule = QPushButton("Annuler")
		annule.clicked.connect(self.reject)
		self.hlayout.addStretch(1)
		self.hlayout.addWidget(annule)
		self.hlayout.addWidget(valide)
		self.vlayout.addLayout(self.hlayout)
		
		screen = QDesktopWidget().availableGeometry()
		coef = 0.6
		self.resize(screen.width()*coef, screen.height()*coef)
		size =  self.geometry()
		self.setGeometry((screen.width() - size.width())/2, (screen.height() - size.height())/2, size.width(), size.height())
	
	def _tabwidget(self):
		settings = QSettings("lheido", "lheidoEdit")
		self.tab = QTabWidget(self)
		# General
		general = QWidget(self)
		general_box = QVBoxLayout(self)
		layout = QGridLayout(self)
		general_box.addLayout(layout)
		general_box.addStretch(1)
		## démarrage
		demarrageTitle = QLabel(u"Démarrage", self)
		demarrageTitle.setObjectName("demarrageTitle")
		path = QLabel(u"Dossier de démarrage", self)
		#~ path.setAlignment(Qt.AlignCenter)
		self.path_edit = QLineEdit(self)
		self.prec_session = QCheckBox(u"Charger la session précédente", self)
		if settings.value("general/prec_session", QVariant(False)).toBool():
			self.prec_session.setCheckState(Qt.Checked)
		else:
			self.prec_session.setCheckState(Qt.Unchecked)
		self.prec_session.setFocusPolicy(Qt.NoFocus)
		## fermeture
		fermetureTitle = QLabel(u"Fermeture", self)
		fermetureTitle.setObjectName("fermetureTitle")
		self.valide_fermeture = QCheckBox("Confirmation avant fermeture", self)
		if settings.value("general/valide_fermeture", QVariant(False)).toBool():
			self.valide_fermeture.setCheckState(Qt.Checked)
		else:
			self.valide_fermeture.setCheckState(Qt.Unchecked)
		self.valide_fermeture.setFocusPolicy(Qt.NoFocus)
		self.save_geo = QCheckBox(u"Enregistrer la position et la géométrie de la fenêtre", self)
		if settings.value("general/save_geo", QVariant(True)).toBool():
			self.save_geo.setCheckState(Qt.Checked)
		else:
			self.save_geo.setCheckState(Qt.Unchecked)
		self.save_geo.setFocusPolicy(Qt.NoFocus)
		
		general_widget = [demarrageTitle, path, self.path_edit, self.prec_session, fermetureTitle, self.valide_fermeture, self.save_geo]
		general_pos = [(0,0,1,2),(1,0),(1,1),(2,0), (3,0,1,2),(4,0),(5,0)]
		for i, elt in enumerate(general_widget):
			layout.addWidget(elt, *general_pos[i])
		general.setLayout(general_box)
		i = self.tab.addTab(general, u"Général")
		self.tab.tabBar().setTabTextColor(i, QColor("#FFFFFF"))
		# Fichiers
		i = self.tab.addTab(QWidget(), u"Fichiers")
		self.tab.tabBar().setTabTextColor(i, QColor("#FFFFFF"))
		# Interface
		#~ interface = QWidget(self)
		#~ interface_box = QVBoxLayout(self)
		#~ font_global_button = QPushButton(u"Police de l'interface", self)
		#~ if settings.value("interface/global_font", QFont()).to
		#~ font_global_button.clicked.connect(self.font_global_dialog)
		#~ font_editor_button = QPushButton(u"Police de l'éditeur", self)
		#~ font_editor_button.clicked.connect(self.font_editor_dialog)
		ui = QWidget(self)
		layout = QVBoxLayout(ui)
		shortcut_ui_label = QLabel("Raccourcis clavier")
		shortcut_ui_label.setObjectName("shortcut_ui_title")
		self.shortcut_ui = ShortcutsTable(False, None)
		layout.addWidget(shortcut_ui_label)
		layout.addWidget(self.shortcut_ui)
		#~ layout.addStretch(1)
		i = self.tab.addTab(ui, u"Interface")
		self.tab.tabBar().setTabTextColor(i, QColor("#FFFFFF"))
		# Editeur
		editeur = QWidget(self)
		editeur_box = QVBoxLayout(self)
		layout = QGridLayout(self)
		editeur_box.addLayout(layout)
		layout.setSpacing(10)
		self.pliage_ch = QCheckBox("Pliage du code", self)
		if settings.value("editeur/pliage", QVariant(True)).toBool():
			self.pliage_ch.setCheckState(Qt.Checked)
		else:
			self.pliage_ch.setCheckState(Qt.Unchecked)
		self.pliage_ch.setFocusPolicy(Qt.NoFocus)
		indentTitle = QLabel("Indentation", self)
		indentTitle.setObjectName("indentTitle")
		tab_width = QLabel("Largeur", self)
		tab_width.setAlignment(Qt.AlignCenter)
		self.tab_width_spin = QSpinBox(self)
		self.tab_width_spin.setRange(0, 10)
		self.tab_width_spin.setValue(settings.value("editeur/indent_width", QVariant(4)).toInt()[0])
		tab_type = QLabel("Type", self)
		tab_type.setAlignment(Qt.AlignCenter)
		self.tab_type_cb = QComboBox(self)
		self.tab_type_cb.addItem("espace")
		self.tab_type_cb.addItem("tabulation")
		self.tab_type_cb.setCurrentIndex(settings.value("editeur/indent_type", QVariant(0)).toInt()[0])
		shortcut_edit_label = QLabel("Raccourcis clavier")
		shortcut_edit_label.setObjectName("shortcut_edit_title")
		self.shortcut_edit = ShortcutsTable()
		edit_widget = [self.pliage_ch, indentTitle, tab_width, self.tab_width_spin, tab_type, self.tab_type_cb, shortcut_edit_label, self.shortcut_edit]
		edit_pos = [(0, 0), (1,0,1,2), (2,0), (2,1), (3,0), (3,1), (4,0,1,2), (5,0,5,2)]
		for i, elt in enumerate(edit_widget):
			layout.addWidget(elt, *edit_pos[i])
		layout.setRowStretch(5, 1)
		editeur.setLayout(editeur_box)
		i = self.tab.addTab(editeur, u"Éditeur")
		self.tab.tabBar().setTabTextColor(i, QColor("#FFFFFF"))
		#~ # Raccourcis
		#~ self.shortcuts_table = ShortcutsTable()
		#~ i = self.tab.addTab(self.shortcuts_table, u"Raccourcis")
		#~ self.tab.tabBar().setTabTextColor(i, QColor("#FFFFFF"))
		self.vlayout.addWidget(self.tab)
	
	def accept(self):
		settings = QSettings("lheido", "lheidoEdit")
		settings.setValue("editeur/indent_width", self.tab_width_spin.value())
		settings.setValue("editeur/indent_type", self.tab_type_cb.currentIndex())
		settings.setValue("editeur/pliage", self.pliage_ch.isChecked())
		settings.setValue("general/save_geo", self.save_geo.isChecked())
		settings.setValue("general/valide_fermeture", self.valide_fermeture.isChecked())
		settings.setValue("general/prec_session", self.prec_session.isChecked())
		#~ settings.setValue("interface/global_font", self.global_font)
		#~ settings.setValue("interface/editor_font", self.editor_font)
		shortcuts_editor = self.shortcut_edit.get_dict()
		for key, val in shortcuts_editor.items():
			settings.setValue("shortcut/{0}".format(key), val)
		shortcuts_ui = self.shortcut_ui.get_dict()
		for key, val in shortcuts_ui.items():
			settings.setValue("shortcut/{0}".format(key), val)
		settings.sync()
		QDialog.accept(self)
	
	def valider(self):
		self.close()
	
	def annuler(self):
		self.close()
	
	def font_global_dialog(self):
		font, ok = QFontDialog.getFont()
		if ok:
			self.setFont(font)
			self.global_font = font
	
	def font_editor_dialog(self):
		font, ok = QFontDialog.getFont()
		if ok:
			self.editor_font = font
	
	def get_settings(self):
		return "settings saved"
		#~ return self.settings
	
	def get_error(self):
		print "annuler"

if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	with open("dev-theme/dev_theme.css") as t:
		dev_theme = t.read()
	app.setStyleSheet(dev_theme)
	dialog = SettingsDialog()
	dialog.show()
	sys.exit(app.exec_())
