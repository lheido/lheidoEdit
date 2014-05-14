#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import QsciScintilla, QsciCommand
import load_lexer

class ShortcutsTable(QTableWidget):
	""" custom widget for manage shortcut """
	UI = {
			"Quit":         ["Ctrl+Q",		u"Quitter l'éditeur"],
			"Open": 	    ["Ctrl+O",		u"Ouvrir un fichier dans le groupe courant"],
			"OpenNewGp":    ["Ctrl+Shift+O",u"Ouvrir un fichier dans un nouveau groupe"],
			"NewFile":      ["Ctrl+N",		u"Nouveau fichier dans le groupe courant"],
			"Save":         ["Ctrl+S",		u"Enregistrer le fichier courant"],
			"SaveAs":       ["Ctrl+Shift+S",u"Enregistrer le fichier courant sous"],
			"ChangeGp":     ["Alt+W",		u"Donne le focus au groupe suivant"],
			"NextTab":      ["Alt+<",		u"Onglet suivant"],
			"PrevTab":      ["Alt+Shift+<",	u"Onglet précédent"],
			"NewGp":        ["Ctrl+B",		u"Nouveau groupe"],
			"TabNextGp":    ["Ctrl+Shift+B",u"Onglet courant vers groupe suivant"],
			"TabPrevGp":    ["Ctrl+Alt+B",	u"Onglet courant vers groupe précédent"],
			"CloseTab":     ["Ctrl+W",		u"Fermer l'onglet courant"],
			"CloseGp":      ["Ctrl+Shift+W",u"Fermer le groupe de l'onglet courant"],
			"ToggleMenuBar":["Ctrl+F1",		u"Afficher/Cacher la barre de menu"],
			"UserPref":     ["Ctrl+Alt+P",	u"Préférences utilisateur"],
			"HighLightM":   ["Ctrl+F2",		u"Outil d'édition de coloration syntaxique"],
			"Execute":      ["F5",			u"Exécuter dans un terminal"] 
	}
	def __init__(self, ui=False, language=False, editor=False, parent=None):
		super(ShortcutsTable, self).__init__(parent)
		self.setSortingEnabled(False)
		header = self.horizontalHeader()
		header.setResizeMode(QHeaderView.Interactive)
		header.setDefaultSectionSize(200)
		self.setAlternatingRowColors(True)
		header.setStretchLastSection(True)
		self.verticalHeader().setVisible(False)
		self.default = None
		if editor:
			self.default = self.editorDefaultCmd()
			self.setColumnCount(3)
			self.setHorizontalHeaderLabels(["id","Raccourcis","Description"])
			self.setColumnHidden(0, True)
			self.shortcut_editor()
		elif ui:
			self.default = self.UI
			self.setColumnCount(3)
			self.setHorizontalHeaderLabels(["id","Raccourcis","Description"])
			self.setColumnHidden(0, True)
			self.shortcut_ui()
		elif language:
			self.setColumnCount(2)
			self.setHorizontalHeaderLabels([u"Langage",u"Règle"])
			self.languages_rules()
		self.itemChanged.connect(self.item_changed)
	
	def editorDefaultCmd(self):
		editor = QsciScintilla()
		cmds = editor.standardCommands().commands()
		return {str(cmd.command()): [QKeySequence(cmd.key()).toString(),cmd.description()] for i, cmd in enumerate(cmds)}
	
	def shortcut_editor(self):
		settings = QSettings("lheido", "lheidoEdit")
		defaultCmds = self.editorDefaultCmd()
		self.id_key = {}
		for i, cmd in enumerate(defaultCmds):
			self.insertRow(self.rowCount())
			key = str(settings.value("shortcut/{0}".format(cmd)).toString())
			#~ key = str(settings.value("shortcut/{0}".format(cmd), defaultCmds[cmd][0]).toString())
			#~ key = str(defaultCmds[cmd][0])
			id_item = QTableWidgetItem()
			id_item.setText(cmd)
			shortcut_item = QTableWidgetItem()
			shortcut_item.setText(key)
			description_item = QTableWidgetItem()
			description_item.setText(defaultCmds[cmd][1])
			description_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled )
			self.setItem(i, 0, id_item)
			self.setItem(i, 1, shortcut_item)
			self.setItem(i, 2, description_item)
			self.id_key[cmd] = [key]
	
	def shortcut_ui(self):
		settings = QSettings("lheido", "lheidoEdit")
		self.id_key = self.UI.copy()
		for i, cmd in enumerate(self.id_key):
			self.insertRow(self.rowCount())
			id_item = QTableWidgetItem()
			id_item.setText(cmd)
			key = str(settings.value("shortcut/{0}".format(cmd), QVariant("{0}".format(self.id_key[cmd][0]))).toString())
			shortcut_item = QTableWidgetItem()
			shortcut_item.setText(key)
			description_item = QTableWidgetItem()
			description_item.setText(self.id_key[cmd][1])
			description_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled )
			self.setItem(i, 0, id_item)
			self.setItem(i, 1, shortcut_item)
			self.setItem(i, 2, description_item)
	
	def languages_rules(self):
		settings = QSettings("lheido", "lheidoEdit")
		self.id_key = {}
		self.lexers = load_lexer.load(["dev-theme/dev_lexers", "custom_lexers"])[0]
		for i, name in enumerate(self.lexers):
			self.insertRow(self.rowCount())
			self.id_key[name] = [str(settings.value("languageRule/{0}".format(name)).toString())]
			language = QTableWidgetItem()
			language.setText(name)
			language.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
			rule = QTableWidgetItem()
			rule.setText(self.id_key[name][0])
			self.setItem(i, 0, language)
			self.setItem(i, 1, rule)
	
	def item_changed(self, item):
		row = self.row(item)
		item_id = str(self.item(row, 0).text())
		new_val = str(item.text())
		existe = False
		if new_val != "":
			for key, val in self.id_key.items():
				if new_val == val[0] and key != item_id:
					existe = True
		self.id_key[item_id][0] = new_val
		color = self.palette().color(QPalette.Base)
		if row % 2 != 0:
			color = self.palette().color(QPalette.AlternateBase)
		if existe:
			color = QColor(200,42,42)
		item.setBackgroundColor(color)
	
	def get_dict(self):
		return self.id_key
	
	def setToDefault(self):
		if self.default is not None:
			for i, key in enumerate(self.default):
				self.item(i, 1).setText(self.default[key][0])
	
class SettingsDialog(QDialog):
	""" Manage user settings """
	def __init__ (self, parent=None):
		super(SettingsDialog, self).__init__(parent)
		self.setWindowTitle(u"Préférences")
		quitter = QAction("Quitter", self)
		quitter.setShortcut("ctrl+Q")
		quitter.triggered.connect(self.reject)
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
		self.shortcut_ui = ShortcutsTable(ui=True)
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
		self.shortcut_edit = ShortcutsTable(editor=True)
		edit_widget = [self.pliage_ch, indentTitle, tab_width, self.tab_width_spin, tab_type, self.tab_type_cb, shortcut_edit_label, self.shortcut_edit]
		edit_pos = [(0, 0), (1,0,1,2), (2,0), (2,1), (3,0), (3,1), (4,0,1,2), (5,0,5,2)]
		for i, elt in enumerate(edit_widget):
			layout.addWidget(elt, *edit_pos[i])
		layout.setRowStretch(5, 1)
		editeur.setLayout(editeur_box)
		i = self.tab.addTab(editeur, u"Éditeur")
		self.tab.tabBar().setTabTextColor(i, QColor("#FFFFFF"))
		# Execute rules
		widget = QWidget(self)
		default_grid = QGridLayout(self)
		default_term_label = QLabel(u"Terminal :", self)
		self.default_term = QLineEdit(self)
		self.default_term.setText(settings.value("default/terminal").toString())
		default_browser_label = QLabel(u"Navigateur :", self)
		self.default_browser = QLineEdit(self)
		self.default_browser.setText(settings.value("default/browser").toString())
		self.rules = ShortcutsTable(language=True)
		default_grid.addWidget(default_term_label, 0, 0)
		default_grid.addWidget(self.default_term, 0, 1)
		default_grid.addWidget(default_browser_label, 1, 0)
		default_grid.addWidget(self.default_browser, 1, 1)
		default_grid.addWidget(self.rules, 2, 0, 2, 2)
		#~ select_layout = QHBoxLayout(self)
		#~ select_language = QLabel(u"Selection du langage")
		#~ select_layout.addWidget(select_language)
		#~ self.language = QComboBox(self)
		#~ self.lexers = load_lexer.load(["dev-theme/dev_lexers", "custom_lexers"])[0]
		#~ for name in self.lexers:
			#~ self.language.addItem(name)
		#~ self.shortcuts_table = ShortcutsTable()
		widget.setLayout(default_grid)
		i = self.tab.addTab(widget, u"Exécuter")
		self.tab.tabBar().setTabTextColor(i, QColor("#FFFFFF"))
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
			settings.setValue("shortcut/{0}".format(key), val[0])
		shortcuts_ui = self.shortcut_ui.get_dict()
		for key, val in shortcuts_ui.items():
			settings.setValue("shortcut/{0}".format(key), val[0])
		rule = self.rules.get_dict()
		for key, val in rule.items():
			settings.setValue("languageRule/{0}".format(key), val[0])
		settings.setValue("default/terminal", self.default_term.text())
		settings.setValue("default/browser", self.default_browser.text())
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
		print "settings saved"
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
