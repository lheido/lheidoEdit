#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

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
		coef = 0.5
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
		#~ font_global_label = QPushButton(u"Police Pour l'interface", self)
		#~ if settings.value("interface/global_font", QFont()).to
		#~ font_global_label.clicked.connect(self.font_global_dialog)
		#~ font_editor_label = QPushButton(u"Police Pour l'éditeur", self)
		#~ font_editor_label.clicked.connect(self.font_editor_dialog)
		i = self.tab.addTab(QWidget(), u"Interface")
		self.tab.tabBar().setTabTextColor(i, QColor("#FFFFFF"))
		# Editeur
		editeur = QWidget(self)
		editeur_box = QVBoxLayout(self)
		layout = QGridLayout(self)
		editeur_box.addLayout(layout)
		editeur_box.addStretch(1)
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
		edit_widget = [self.pliage_ch, indentTitle, tab_width, self.tab_width_spin, tab_type, self.tab_type_cb]
		edit_pos = [(0, 0), (1,0,1,2), (2,0), (2,1), (3,0), (3,1)]
		for i, elt in enumerate(edit_widget):
			layout.addWidget(elt, *edit_pos[i])
		editeur.setLayout(editeur_box)
		i = self.tab.addTab(editeur, u"Éditeur")
		self.tab.tabBar().setTabTextColor(i, QColor("#FFFFFF"))
		# Raccourcis
		i = self.tab.addTab(QWidget(), u"Raccourcis")
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
