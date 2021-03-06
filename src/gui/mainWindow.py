# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
from ..logic import core
from . import Editor
from . import tabla
from . import treeView
import src.logic.helper


class nPy(QtGui.QMainWindow):
    def __init__(self):
        super(nPy, self).__init__()
        self.setWindowTitle('Nuclear Py - Instituto de Tecnologia Nuclear Dan Beninson')
        self.treeWidget = treeView.TreeView(self)
        self.crearIndicadorSecuencia()
        self.crearTerminal()
        self.ventanaPrincipal()
        self.crearMenu()
        self.statusBar()
        self.show()

    def crearIndicadorSecuencia(self):
        self.font = QtGui.QFont()
        self.font.setFamily("Consolas, 'Courier New', monospace")
        self.font.setPointSize(11)  # font size in points
        self.indicadorSecuencia = QtGui.QTextEdit(self)
        self.indicadorSecuencia.setReadOnly(True)
        self.indicadorSecuencia.setFont(self.font)
        self.indicadorSecuencia.setMaximumHeight(800)
        self.indicadorSecuencia.setFontWeight(75)  # 50 normal, 75 BOLD

    def crearTerminal(self):
        self.terminalOutput = QtGui.QTextEdit(self)
        self.terminalOutput.setReadOnly(True)
        self.terminalOutput.setFont(self.font)
        self.terminalOutput.setStyleSheet("background-color: #585858; color: #fff")
        self.terminalOutput.setMaximumHeight(1000)
        self.cursor = self.terminalOutput.textCursor()

    def ventanaPrincipal(self):
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.killButton = QtGui.QPushButton("Kill process")
        self.killButton.clicked.connect(self.KillingProcess)
        self.copyOutputButton = QtGui.QPushButton("Copy to editor")
        self.copyOutputButton.clicked.connect(self.copyOutputToEditor)
        self.cleanTerminalButton = QtGui.QPushButton("Clean terminal")
        self.cleanTerminalButton.clicked.connect(self.cleanTerminal)
        self.killGo = QtGui.QPushButton("Exit app")
        self.killGo.clicked.connect(self.quitApp)
        self.terminalOutput.setMinimumHeight(100)
        self.cursor = QtGui.QTextCursor(self.terminalOutput.document())
        widget_central = QtGui.QWidget(self)
        self.setCentralWidget(widget_central)
        layout = QtGui.QVBoxLayout(widget_central)
        self.tabWidget = QtGui.QTabWidget()
        self.tabOutputs = QtGui.QWidget()
        self.tabEditor = Editor.Editor()
        self.tabApplication = QtGui.QWidget()
        self.tabConfiguracion = QtGui.QTabWidget()

        self.configTab1 = QtGui.QWidget()
        self.configTab2 = QtGui.QWidget()
        self.configTab3 = QtGui.QWidget()
        self.configTab4 = QtGui.QWidget()

        BotoneraInferior = QtGui.QHBoxLayout()  # widget_central
        BotoneraInferior.addWidget(self.killGo)
        self.tabWidget.addTab(self.tabOutputs, "Process")
        self.tabWidget.addTab(self.tabEditor, "Text Editor")
        layoutTab1 = QtGui.QVBoxLayout(self.tabWidget)
        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.indicadorCWD = QtGui.QLabel("<html>Working on <b>" + core.getTreeViewInitialPath() +
                                         "</b> - Treeview on <b>" + core.getTreeViewRootPath() + "</b></html>")
        self.indicadorSecuenciaNombre = QtGui.QLabel('<html><b>Current process</b></html>')
        self.terminalOutputNombre = QtGui.QLabel('<html><b>Standard output</b></html>')
        layoutSecuencia = QtGui.QVBoxLayout()
        layoutSecuencia.addWidget(self.indicadorCWD)
        layoutSecuencia.addWidget(self.indicadorSecuenciaNombre)
        layoutSecuencia.addWidget(self.indicadorSecuencia)
        unWidget = QtGui.QWidget()
        unWidget.setLayout(layoutSecuencia)
        splitter.addWidget(unWidget)
        otroWidget = QtGui.QWidget()
        layoutTerminal = QtGui.QVBoxLayout()
        layoutTerminal.addWidget(self.terminalOutputNombre)
        layoutTerminal.addWidget(self.terminalOutput)
        otroWidget.setLayout(layoutTerminal)
        splitter.addWidget(otroWidget)
        layoutTab1.addWidget(splitter)

        layoutButtons = QtGui.QHBoxLayout()
        buttonsWidget = QtGui.QWidget()
        layoutButtons.addWidget(self.killButton)
        layoutButtons.addWidget(self.copyOutputButton)
        layoutButtons.addWidget(self.cleanTerminalButton)
        buttonsWidget.setLayout(layoutButtons)

        layoutTab1.addWidget(buttonsWidget)

        self.tabOutputs.setLayout(layoutTab1)

        self.tabWidget.addTab(self.tabApplication, "Application")
        layoutTabsConfig = QtGui.QVBoxLayout(self.tabApplication)
        layoutTabsConfig.addWidget(self.tabConfiguracion)
        self.tabApplication.setLayout(layoutTabsConfig)
        self.tabConfiguracion.addTab(self.configTab1, "Sequence Table")
        self.tabConfiguracion.addTab(self.configTab4, "Environment")

        self.dirRoot = QtGui.QLabel('Treeview path')
        self.dirInitial = QtGui.QLabel('Working directory')

        self.dirButtonFindDirCWD = QtGui.QPushButton("Update")
        self.dirButtonFindDirRoot = QtGui.QPushButton("Update")

        viewInitialPath = core.getTreeViewInitialPath()
        viewRootPath = core.getTreeViewRootPath()

        self.dirRootEdit = QtGui.QLineEdit(str(viewRootPath))
        self.dirInitialEdit = QtGui.QLineEdit(str(viewInitialPath))

        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(16)

        self.grid.addWidget(self.dirRoot, 1, 0)			        # Titulo
        self.grid.addWidget(self.dirRootEdit, 1, 1)		        # Campo de texto
        self.grid.addWidget(self.dirButtonFindDirRoot, 1, 2)  # Boton Dir
        self.grid.addWidget(self.dirInitial, 2, 0)			    # Titulo
        self.grid.addWidget(self.dirInitialEdit, 2, 1)          # Campo de texto
        self.grid.addWidget(self.dirButtonFindDirCWD, 2, 2)     # Boton Dir

        self.dirButtonFindDirCWD.clicked.connect(self.getDirNameInit)
        self.dirButtonFindDirRoot.clicked.connect(self.getDirNameRoot)

        self.configTab4.setLayout(self.grid)

        layoutTab3 = QtGui.QVBoxLayout(self.tabWidget)
        self.tabla = tabla.Tabla()
        self.tabla.ShowDataSet(core.fullDataSet(), core.getHeaders())
        self.addRowButton = QtGui.QPushButton("Add row")
        self.addRowButton.clicked.connect(self.tabla.addRow)
        self.delRowButton = QtGui.QPushButton("Delete current row")
        self.delRowButton.clicked.connect(self.tabla.delRow)
        self.saveTableButton = QtGui.QPushButton("Save changes")
        self.saveTableButton.clicked.connect(self.guardarCambiosClicked)
        layoutTab3.addWidget(self.tabla)

        # layoutTab3.addWidget(self.addRowButton)
        # layoutTab3.addWidget(self.delRowButton)
        # layoutTab3.addWidget(self.saveTableButton)

        layoutButtonsTab = QtGui.QHBoxLayout()
        layoutButtonsTab.addWidget(self.addRowButton)
        layoutButtonsTab.addWidget(self.delRowButton)
        layoutButtonsTab.addWidget(self.saveTableButton)
        buttonsTabWidget = QtGui.QWidget()
        buttonsTabWidget.setLayout(layoutButtonsTab)

        layoutTab3.addWidget(buttonsTabWidget)
        self.configTab1.setLayout(layoutTab3)

        splitterHoriz = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitterHoriz.addWidget(self.treeWidget)
        splitterHoriz.addWidget(self.tabWidget)
        layout.addWidget(splitterHoriz)
        layout.addLayout(BotoneraInferior)
        self.show()
        sizes = splitterHoriz.sizes()
        splitterHoriz.setSizes([sizes[0] * 0.7, sizes[1]])

    def crearMenu(self):
        self.menuBar().clear()
        menubar = self.menuBar()
        for menu in core.menuList(core.fullDataSet()):
            thisMenu = menubar.addMenu('&' + str(menu))
            for subMenu, idFila in zip(core.subMenuList(menu, core.fullDataSet()), core.idList(menu, core.fullDataSet())):
                action = QtGui.QAction('&' + str(subMenu), self)
                action.setStatusTip(str(idFila) + " - " + str(subMenu))
                action.triggered.connect(lambda ignore, idt=subMenu: self.subMenuOptionClicked(idt))
                thisMenu.addAction(action)

    def actualizarCWD(self):
        core.updateCfgPath(self.dirInitialEdit.text(), 0)
        self.currentDirectories()
        self.treeWidget.updateTreeView()

    def actualizarRootPath(self):
        core.updateCfgPath(self.dirRootEdit.text(), 1)
        self.currentDirectories()
        self.treeWidget.updateTreeView()

    def subMenuOptionClicked(self, subMenu):
        core.PreEjecutarComandos(subMenu, self)

    def showOutputInTerminal(self, text):
        self.terminalOutput.append(text)

    def KillingProcess(self):
        self.terminalOutput.append("Killing process:")
        core.matarProceso(self)

    def cleanTerminal(self):
        self.terminalOutput.clear()
        self.indicadorSecuencia.clear()
        self.indicadorSecuencia.setText("")

    def guardarCambiosClicked(self):
        core.saveTable(self.tabla)
        self.crearMenu()
        self.tabWidget.setCurrentIndex(0)
        self.terminalOutput.setText("Se actualizo la tabla de secuencias")

    def quitApp(self):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure you want to quit?",
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            sys.exit()

    def getDirNameRoot(self):
        filename = QtGui.QFileDialog.getExistingDirectory(
            directory=src.logic.helper.getTreeViewInitialPath())
        if filename:
            self.dirRootEdit.setText(filename)
            self.actualizarRootPath()

    def getDirNameInit(self):
        filename = QtGui.QFileDialog.getExistingDirectory(
            directory=src.logic.helper.getTreeViewInitialPath())
        if filename:
            self.dirInitialEdit.setText(filename)
            self.actualizarCWD()

    def currentDirectories(self):
        directoriesUpdated = str("<html>Working on <b>" + core.getTreeViewInitialPath() +
                                 "</b> - Treeview on <b>" + core.getTreeViewRootPath() + "</b></html>")
        self.indicadorCWD.setText(directoriesUpdated)
        self.terminalOutput.setText(directoriesUpdated)

    def copyOutputToEditor(self):
        outputString = self.terminalOutput.toPlainText()
        indiceNuevo = self.tabEditor.newEditorTab()
        self.tabEditor.tabWidget.widget(indiceNuevo).setPlainText(outputString)
        self.tabWidget.setCurrentIndex(1)
