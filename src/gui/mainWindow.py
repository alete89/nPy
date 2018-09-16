# -*- coding: utf-8 -*-
import sys
import os
from PyQt4 import QtGui, QtCore
from ..logic import core
from . import Highlighter
from . import CodeEditor
from . import tabla
from . import treeView


class PyCGI(QtGui.QMainWindow):
    def __init__(self):
        super(PyCGI, self).__init__()
        self.is_new = True  # Flag para el archivo del editor
        self.file_name = ''  # Nombre del archivo del editor
        self.setWindowTitle('PyCGI - Instituto de Tecnologia Nuclear Dan Beninson')
        self.treeWidget = treeView.TreeView(self)
        self.crearIndicadorSecuencia()
        self.crearTerminal()
        self.crearEditorDeTexto()
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
        self.indicadorSecuencia.setMaximumHeight(50)
        self.indicadorSecuencia.setFontWeight(75)  # 50 normal, 75 BOLD

    def crearTerminal(self):
        self.terminalOutput = QtGui.QTextEdit(self)
        self.terminalOutput.setReadOnly(True)
        self.terminalOutput.setFont(self.font)
        self.terminalOutput.setStyleSheet("background-color: #585858; color: #fff")
        self.cursor = self.terminalOutput.textCursor()

    def crearEditorDeTexto(self):
        self.EditorDeTexto = CodeEditor.CodeEditor()
        self.EditorDeTexto.setFont(self.font)
        self.EditorDeTexto.setStyleSheet("background-color: #f1f1f1;")
        self.EditorDeTexto.setMinimumHeight(100)
        self.highlighter = Highlighter.Highlighter(self.EditorDeTexto.document())
        self.highlighter.setDocument(None)

    def crearToolbar(self):
        toolbar = self.addToolBar("Text editor - Toolbar")
        
        NewOne = QtGui.QAction(QtGui.QIcon('icons/new.png'), 'New', self)
        NewOne.setShortcut('Ctrl+n')
        NewOne.setStatusTip("New file")
        NewOne.triggered.connect(self.newEditorTab)
        toolbar.addAction(NewOne)
        
        OpenIcon = QtGui.QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
        OpenIcon.setShortcut('Ctrl+o')
        OpenIcon.setStatusTip("Open file")
        OpenIcon.triggered.connect(self.openFile)
        toolbar.addAction(OpenIcon)
        
        SaveIcon = QtGui.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
        SaveIcon.setShortcut('Ctrl+s')
        SaveIcon.setStatusTip("Save file")
        SaveIcon.triggered.connect(self.saveDialog)
        toolbar.addAction(SaveIcon)
        
        SaveAsIcon = QtGui.QAction(QtGui.QIcon('icons/saveAs.png'), 'Save as', self)
        SaveAsIcon.setShortcut('Ctrl+g')
        SaveAsIcon.setStatusTip("Save as")
        SaveAsIcon.triggered.connect(self.saveAsDialog)
        toolbar.addAction(SaveAsIcon)
        
        CloseIcon = QtGui.QAction(QtGui.QIcon('icons/closeFile.png'), 'Close', self)
        CloseIcon.setShortcut('Ctrl+x')
        CloseIcon.setStatusTip("Close file")
        CloseIcon.triggered.connect(self.CloseDialog)
        toolbar.addAction(CloseIcon)
        return toolbar

    def ventanaPrincipal(self):
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.killButton = QtGui.QPushButton("Kill process")
        self.killButton.clicked.connect(self.KillingProcess)
        self.cleanTerminalButton = QtGui.QPushButton("Clean terminal")
        self.cleanTerminalButton.clicked.connect(self.cleanTerminal)
        self.killGo = QtGui.QPushButton("Exit app")
        self.killGo.clicked.connect(self.quitApp)
        self.terminalOutput.setMinimumHeight(100)
        self.cursor = QtGui.QTextCursor(self.terminalOutput.document())
        widget_central = QtGui.QWidget(self)
        self.setCentralWidget(widget_central)
        layout = QtGui.QVBoxLayout(widget_central)
        self.tabs = QtGui.QTabWidget()
        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()
        self.tabsInternas = QtGui.QTabWidget()
        self.tabsConfiguracion = QtGui.QTabWidget()
        self.configTab1 = QtGui.QWidget()
        self.configTab2 = QtGui.QWidget()
        self.configTab3 = QtGui.QWidget()
        BotoneraInferior = QtGui.QHBoxLayout(widget_central)
        BotoneraInferior.addWidget(self.killGo)
        self.tabs.addTab(self.tab1, "Process")
        self.tabs.addTab(self.tab2, "Text Editor")
        layoutTab1 = QtGui.QVBoxLayout(self.tabs)
        layoutTab1.addWidget(self.indicadorSecuencia)
        layoutTab1.addWidget(self.terminalOutput)
        layoutTab1.addWidget(self.killButton)
        layoutTab1.addWidget(self.cleanTerminalButton)
        self.tab1.setLayout(layoutTab1)
        layoutTab2 = QtGui.QVBoxLayout(self.tabs)
        layoutTab2.addWidget(self.crearToolbar())
        self.tab2.setLayout(layoutTab2)
        self.tabs.addTab(self.tab3, "Configuration")
        layoutTabsConfig = QtGui.QVBoxLayout(self.tab3)
        layoutTabsConfig.addWidget(self.tabsConfiguracion)
        self.tab3.setLayout(layoutTabsConfig)
        self.tabsConfiguracion.addTab(self.configTab1, "Sequence Table")
        self.tabsConfiguracion.addTab(self.configTab2, "Global Variables")
        self.tabsConfiguracion.addTab(self.configTab3, "Import")
        layoutTab2.addWidget(self.tabsInternas)
        layoutTab3 = QtGui.QVBoxLayout(self.tabs)
        self.tabla = tabla.Tabla()
        self.tabla.ShowDataSet(core.fullDataSet(), core.getHeaders())
        self.addRowButton = QtGui.QPushButton("Add row")
        self.addRowButton.clicked.connect(self.tabla.addRow)
        self.delRowButton = QtGui.QPushButton("Delete current row")
        self.delRowButton.clicked.connect(self.tabla.delRow)
        self.saveTableButton = QtGui.QPushButton("Save changes")
        self.saveTableButton.clicked.connect(self.guardarCambiosClicked)
        layoutTab3.addWidget(self.tabla)
        layoutTab3.addWidget(self.addRowButton)
        layoutTab3.addWidget(self.delRowButton)
        layoutTab3.addWidget(self.saveTableButton)
        self.configTab1.setLayout(layoutTab3)
        splitterHoriz = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitterHoriz.addWidget(self.treeWidget)
        splitterHoriz.addWidget(self.tabs)
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

    def guardarCambiosClicked(self):
        core.saveTable(self.tabla)
        self.crearMenu()

    def quitApp(self):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure you want to quit?",
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            sys.exit()

    def newEditorTab(self, fname):
        if not fname:
            newTabName = 'Temp'
        else:
            if os.path.isfile(fname):
                newTabName = str(fname)

        newTab = QtGui.QWidget()
        self.tabsInternas.addTab(newTab, str(newTabName))
        newTabLayout = QtGui.QVBoxLayout(newTab)
        self.crearEditorDeTexto()
        newTabLayout.addWidget(self.EditorDeTexto)
        newTab.setLayout(newTabLayout)
        self.tabsInternas.setCurrentWidget(newTab)

    def openFile(self, fname):
        if not fname:
            fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname:
            with open(fname, 'r') as f:
                self.newEditorTab(fname)
                data = f.read()
                self.EditorDeTexto.setPlainText(data)
                self.is_new = False
                self.file_name = fname
        if fname[-3:] == ".py":
            self.highlighter.setDocument(self.EditorDeTexto.document())

    def saveAsDialog(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File', str(self.file_name))
        if name:
            textoParaGuardar = self.EditorDeTexto.toPlainText()
            with open(name, "w") as nFile:
                nFile.write(textoParaGuardar)
                self.is_new = False
                self.file_name = name

    def saveDialog(self):
        if self.is_new:
            self.saveAsDialog()
        else:
            textoParaGuardar = self.EditorDeTexto.toPlainText()
            with open(self.file_name, "w") as nFile:
                nFile.write(textoParaGuardar)

    def removeTabFile(self):
        self.tabsInternas.removeTab(self.tabsInternas.currentIndex())

    def CloseDialog(self):
        if self.is_new:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setText(u"The file has been modified.")
            msg.setInformativeText("Save the changes?")
            msg.setStandardButtons(QtGui.QMessageBox.Save |
                                   QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
            resultado = msg.exec_()
            if resultado == QtGui.QMessageBox.Save:
                self.saveDialog()
            elif resultado == QtGui.QMessageBox.Discard:
                self.removeTabFile()
            elif resultado == QtGui.QMessageBox.Cancel:
                return
        else:
            self.removeTabFile()
        cursor.setPosition(start)
        cursor.movePosition(cursor.StartOfLine)
        start = cursor.position()


        while cursor.position() < end:
            global var
            
            cursor.movePosition(cursor.StartOfLine)
            cursor.deleteChar()
            cursor.movePosition(cursor.EndOfLine)
            cursor.movePosition(cursor.Down)
            end -= len(tab)

            '''if cursor.position() == end:
                var +=1

            if var == 2:
                break'''

    def CursorPosition(self):
        line = self.EditorDeTexto.textCursor().blockNumber()
        col = self.EditorDeTexto.textCursor().columnNumber()
        linecol = ("Line: "+str(line)+" | "+"Column: "+str(col))
        self.status.showMessage(linecol)

    def Find(self):
        global f
        
        find = Find(self)
        find.show()

        def handleFind():

            f = find.te.toPlainText()
            print(f)
            
            if cs == True and wwo == False:
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindCaseSensitively
                
            elif cs == False and wwo == False:
                flag = QtGui.QTextDocument.FindBackward
                
            elif cs == False and wwo == True:
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindWholeWords
                
            elif cs == True and wwo == True:
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindCaseSensitively and QtGui.QTextDocument.FindWholeWords
            
            self.EditorDeTexto.find(f,flag)

        def handleReplace():
            f = find.te.toPlainText()
            r = find.rp.toPlainText()

            text = self.EditorDeTexto.toPlainText()
            
            newText = EditorDeTexto.replace(f,r)

            self.EditorDeTexto.clear()
            self.EditorDeTexto.append(newText)
        
        find.src.clicked.connect(handleFind)
        find.rpb.clicked.connect(handleReplace)
        
    def PageView(self):
        preview = QtGui.QPrintPreviewDialog()
        preview.paintRequested.connect(self.PaintPageView)
        preview.exec_()

    def PaintPageView(self, printer):
        self.EditorDeTexto.print_(printer)
        
    def Print(self):
        dialog = QtGui.QPrintDialog()
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.EditorDeTexto.document().print_(dialog.printer())

    def ventanaPrincipal(self):
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.killButton = QtGui.QPushButton("Kill process")
        self.killButton.clicked.connect(self.KillingProcess)
        self.cleanTerminalButton = QtGui.QPushButton("Clean terminal")
        self.cleanTerminalButton.clicked.connect(self.cleanTerminal)
        self.killGo = QtGui.QPushButton("Exit app")
        self.killGo.clicked.connect(self.quitApp)
        self.terminalOutput.setMinimumHeight(100)
        self.cursor = QtGui.QTextCursor(self.terminalOutput.document())
        widget_central = QtGui.QWidget(self)
        self.setCentralWidget(widget_central)
        layout = QtGui.QVBoxLayout(widget_central)
        self.tabs = QtGui.QTabWidget()
        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()
        self.tabsInternas = QtGui.QTabWidget()
        self.tabsConfiguracion = QtGui.QTabWidget()
        self.configTab1 = QtGui.QWidget()
        self.configTab2 = QtGui.QWidget()
        self.configTab3 = QtGui.QWidget()
        BotoneraInferior = QtGui.QHBoxLayout(widget_central)
        BotoneraInferior.addWidget(self.killGo)
        self.tabs.addTab(self.tab1, "Process")
        self.tabs.addTab(self.tab2, "Text Editor")
        layoutTab1 = QtGui.QVBoxLayout(self.tabs)
        layoutTab1.addWidget(self.indicadorSecuencia)
        layoutTab1.addWidget(self.terminalOutput)
        layoutTab1.addWidget(self.killButton)
        layoutTab1.addWidget(self.cleanTerminalButton)
        self.tab1.setLayout(layoutTab1)
        layoutTab2 = QtGui.QVBoxLayout(self.tabs)
        layoutTab2.addWidget(self.crearToolbar())
        self.tab2.setLayout(layoutTab2)
        self.tabs.addTab(self.tab3, "Configuration")
        layoutTabsConfig = QtGui.QVBoxLayout(self.tab3)
        layoutTabsConfig.addWidget(self.tabsConfiguracion)
        self.tab3.setLayout(layoutTabsConfig)
        self.tabsConfiguracion.addTab(self.configTab1, "Sequence Table")
        self.tabsConfiguracion.addTab(self.configTab2, "Global Variables")
        self.tabsConfiguracion.addTab(self.configTab3, "Import")
        layoutTab2.addWidget(self.tabsInternas)
        layoutTab3 = QtGui.QVBoxLayout(self.tabs)
        self.tabla = tabla.Tabla()
        self.tabla.ShowDataSet(core.fullDataSet(), core.getHeaders())
        self.addRowButton = QtGui.QPushButton("Add row")
        self.addRowButton.clicked.connect(self.tabla.addRow)
        self.delRowButton = QtGui.QPushButton("Delete current row")
        self.delRowButton.clicked.connect(self.tabla.delRow)
        self.saveTableButton = QtGui.QPushButton("Save changes")
        self.saveTableButton.clicked.connect(self.guardarCambiosClicked)
        layoutTab3.addWidget(self.tabla)
        layoutTab3.addWidget(self.addRowButton)
        layoutTab3.addWidget(self.delRowButton)
        layoutTab3.addWidget(self.saveTableButton)
        self.configTab1.setLayout(layoutTab3)
        splitterHoriz = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitterHoriz.addWidget(self.treeWidget)
        splitterHoriz.addWidget(self.tabs)
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

    def guardarCambiosClicked(self):
        core.saveTable(self.tabla)
        self.crearMenu()

    def quitApp(self):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure you want to quit?",
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            sys.exit()

    def newEditorTab(self, fname):
        if not fname:
            newTabName = 'Temp'
        else:
            if os.path.isfile(fname):
                newTabName = str(fname)

        newTab = QtGui.QWidget()

        NuevaTab=self.tabsInternas.addTab(newTab, str(newTabName))
        self.tabsInternas.setTabsClosable(True)
#        QtCore.QObject.connect(NuevaTab, QtCore.SIGNAL("clicked()"), self.CloseDialog)
        newTabLayout = QtGui.QVBoxLayout(newTab)
        self.crearEditorDeTexto()
        newTabLayout.addWidget(self.EditorDeTexto)
        newTab.setLayout(newTabLayout)
        self.tabsInternas.setCurrentWidget(newTab)

    def openFile(self, fname):
        if not fname:
            fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname:
            with open(fname, 'r') as f:
                self.newEditorTab(fname)
                data = f.read()
                self.EditorDeTexto.setPlainText(data)
                self.is_new = False
                self.file_name = fname
        if fname[-3:] == ".py":
            self.highlighter.setDocument(self.EditorDeTexto.document())

    def saveAsDialog(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File', str(self.file_name))
        if name:
            textoParaGuardar = self.EditorDeTexto.toPlainText()
            with open(name, "w") as nFile:
                nFile.write(textoParaGuardar)
                self.is_new = False
                self.file_name = name

    def saveDialog(self):
        if self.is_new:
            self.saveAsDialog()
        else:
            textoParaGuardar = self.EditorDeTexto.toPlainText()
            with open(self.file_name, "w") as nFile:
                nFile.write(textoParaGuardar)

    def removeTabFile(self):
        self.tabsInternas.removeTab(self.tabsInternas.currentIndex())

    def CloseDialog(self):
        if self.is_new:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setText(u"The file has been modified.")
            msg.setInformativeText("Save the changes?")
            msg.setStandardButtons(QtGui.QMessageBox.Save |
                                   QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
            resultado = msg.exec_()
            if resultado == QtGui.QMessageBox.Save:
                self.saveDialog()
            elif resultado == QtGui.QMessageBox.Discard:
                self.removeTabFile()
            elif resultado == QtGui.QMessageBox.Cancel:
                return
        else:
            self.removeTabFile()
        cursor.setPosition(start)
        cursor.movePosition(cursor.StartOfLine)
        start = cursor.position()


        while cursor.position() < end:
            global var
            
            cursor.movePosition(cursor.StartOfLine)
            cursor.deleteChar()
            cursor.movePosition(cursor.EndOfLine)
            cursor.movePosition(cursor.Down)
            end -= len(tab)

            '''if cursor.position() == end:
                var +=1

            if var == 2:
                break'''

    def CursorPosition(self):
        line = self.EditorDeTexto.textCursor().blockNumber()
        col = self.EditorDeTexto.textCursor().columnNumber()
        linecol = ("Line: "+str(line)+" | "+"Column: "+str(col))
        self.status.showMessage(linecol)

    def Find(self):
        global f
        
        find = Find(self)
        find.show()

        def handleFind():

            f = find.te.toPlainText()
            print(f)
            
            if cs == True and wwo == False:
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindCaseSensitively
                
            elif cs == False and wwo == False:
                flag = QtGui.QTextDocument.FindBackward
                
            elif cs == False and wwo == True:
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindWholeWords
                
            elif cs == True and wwo == True:
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindCaseSensitively and QtGui.QTextDocument.FindWholeWords
            
            self.EditorDeTexto.find(f,flag)

        def handleReplace():
            f = find.te.toPlainText()
            r = find.rp.toPlainText()

            text = self.EditorDeTexto.toPlainText()
            
            newText = EditorDeTexto.replace(f,r)

            self.EditorDeTexto.clear()
            self.EditorDeTexto.append(newText)
        
        find.src.clicked.connect(handleFind)
        find.rpb.clicked.connect(handleReplace)
        
    def PageView(self):
        preview = QtGui.QPrintPreviewDialog()
        preview.paintRequested.connect(self.PaintPageView)
        preview.exec_()

    def PaintPageView(self, printer):
        self.EditorDeTexto.print_(printer)
        
    def Print(self):
        dialog = QtGui.QPrintDialog()
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.EditorDeTexto.document().print_(dialog.printer())

    def ventanaPrincipal(self):
        self.setMinimumWidth(350)
        self.setMinimumHeight(300)
        self.killButton = QtGui.QPushButton("Kill process")
        self.killButton.clicked.connect(self.KillingProcess)
        self.cleanTerminalButton = QtGui.QPushButton("Clean terminal")
        self.cleanTerminalButton.clicked.connect(self.cleanTerminal)
        self.killGo = QtGui.QPushButton("Exit app")
        self.killGo.clicked.connect(self.quitApp)
        self.terminalOutput.setMinimumHeight(100)
        self.cursor = QtGui.QTextCursor(self.terminalOutput.document())
        widget_central = QtGui.QWidget(self)
        self.setCentralWidget(widget_central)
        layout = QtGui.QVBoxLayout(widget_central)
        self.tabs = QtGui.QTabWidget()
        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()
        self.tabsInternas = QtGui.QTabWidget()
        self.tabsConfiguracion = QtGui.QTabWidget()
        self.configTab1 = QtGui.QWidget()
        self.configTab2 = QtGui.QWidget()
        self.configTab3 = QtGui.QWidget()
        BotoneraInferior = QtGui.QHBoxLayout(widget_central)
        BotoneraInferior.addWidget(self.killGo)
        self.tabs.addTab(self.tab1, "Process")
        self.tabs.addTab(self.tab2, "Text Editor")
        layoutTab1 = QtGui.QVBoxLayout(self.tabs)
        layoutTab1.addWidget(self.indicadorSecuencia)
        layoutTab1.addWidget(self.terminalOutput)
        layoutTab1.addWidget(self.killButton)
        layoutTab1.addWidget(self.cleanTerminalButton)
        self.tab1.setLayout(layoutTab1)
        layoutTab2 = QtGui.QVBoxLayout(self.tabs)
        layoutTab2.addWidget(self.crearToolbar())
        self.tab2.setLayout(layoutTab2)
        self.tabs.addTab(self.tab3, "Configuration")
        layoutTabsConfig = QtGui.QVBoxLayout(self.tab3)
        layoutTabsConfig.addWidget(self.tabsConfiguracion)
        self.tab3.setLayout(layoutTabsConfig)
        self.tabsConfiguracion.addTab(self.configTab1, "Sequence Table")
        self.tabsConfiguracion.addTab(self.configTab2, "Global Variables")
        self.tabsConfiguracion.addTab(self.configTab3, "Import")
        layoutTab2.addWidget(self.tabsInternas)
        layoutTab3 = QtGui.QVBoxLayout(self.tabs)
        self.tabla = tabla.Tabla()
        self.tabla.ShowDataSet(core.fullDataSet(), core.getHeaders())
        self.addRowButton = QtGui.QPushButton("Add row")
        self.addRowButton.clicked.connect(self.tabla.addRow)
        self.delRowButton = QtGui.QPushButton("Delete current row")
        self.delRowButton.clicked.connect(self.tabla.delRow)
        self.saveTableButton = QtGui.QPushButton("Save changes")
        self.saveTableButton.clicked.connect(self.guardarCambiosClicked)
        layoutTab3.addWidget(self.tabla)
        layoutTab3.addWidget(self.addRowButton)
        layoutTab3.addWidget(self.delRowButton)
        layoutTab3.addWidget(self.saveTableButton)
        self.configTab1.setLayout(layoutTab3)
        splitterHoriz = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitterHoriz.addWidget(self.treeWidget)
        splitterHoriz.addWidget(self.tabs)
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

    def guardarCambiosClicked(self):
        core.saveTable(self.tabla)
        self.crearMenu()

    def quitApp(self):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure you want to quit?",
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            sys.exit()

    def newEditorTab(self, fname):
        if not fname:
            newTabName = 'Temp'
        else:
            if os.path.isfile(fname):
                newTabName = str(fname)

        newTab = QtGui.QWidget()

        NuevaTab=self.tabsInternas.addTab(newTab, str(newTabName))
        self.tabsInternas.setTabsClosable(True)
#        QtCore.QObject.connect(NuevaTab, QtCore.SIGNAL("clicked()"), self.CloseDialog)
        newTabLayout = QtGui.QVBoxLayout(newTab)
        self.crearEditorDeTexto()
        newTabLayout.addWidget(self.EditorDeTexto)
        newTab.setLayout(newTabLayout)
        self.tabsInternas.setCurrentWidget(newTab)

    def openFile(self, fname):
        if not fname:
            fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname:
            with open(fname, 'r') as f:
                self.newEditorTab(fname)
                data = f.read()
                self.EditorDeTexto.setPlainText(data)
                self.is_new = False
                self.file_name = fname
        if fname[-3:] == ".py":
            self.highlighter.setDocument(self.EditorDeTexto.document())

    def saveAsDialog(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File', str(self.file_name))
        if name:
            textoParaGuardar = self.EditorDeTexto.toPlainText()
            with open(name, "w") as nFile:
                nFile.write(textoParaGuardar)
                self.is_new = False
                self.file_name = name

    def saveDialog(self):
        if self.is_new:
            self.saveAsDialog()
        else:
            textoParaGuardar = self.EditorDeTexto.toPlainText()
            with open(self.file_name, "w") as nFile:
                nFile.write(textoParaGuardar)

    def removeTabFile(self):
        self.tabsInternas.removeTab(self.tabsInternas.currentIndex())

    def CloseDialog(self):
        if self.is_new:
            msg = QtGui.QMessageBox()
            msg.setIcon(QtGui.QMessageBox.Warning)
            msg.setText(u"The file has been modified.")
            msg.setInformativeText("Save the changes?")
            msg.setStandardButtons(QtGui.QMessageBox.Save |
                                   QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
            resultado = msg.exec_()
            if resultado == QtGui.QMessageBox.Save:
                self.saveDialog()
            elif resultado == QtGui.QMessageBox.Discard:
                self.removeTabFile()
            elif resultado == QtGui.QMessageBox.Cancel:
                return
        else:
            self.removeTabFile()

#---- clase de busqueda -------------------------------------

class Find(QtGui.QDialog):
    def __init__(self,parent = None):
        QtGui.QDialog.__init__(self, parent)
        
        self.initUI()

    def initUI(self):

        self.lb1 = QtGui.QLabel("Search for: ",self)
        self.lb1.setStyleSheet("font-size: 15px; ")
        self.lb1.move(10,10)

        self.te = QtGui.QTextEdit(self)
        self.te.move(10,40)
        self.te.resize(250,25)

        self.src = QtGui.QPushButton("Find",self)
        self.src.move(270,40)

        self.lb2 = QtGui.QLabel("Replace all by: ",self)
        self.lb2.setStyleSheet("font-size: 15px; ")
        self.lb2.move(10,80)

        self.rp = QtGui.QTextEdit(self)
        self.rp.move(10,110)
        self.rp.resize(250,25)

        self.rpb = QtGui.QPushButton("Replace",self)
        self.rpb.move(270,110)

        self.opt1 = QtGui.QCheckBox("Case sensitive",self)
        self.opt1.move(10,160)
        self.opt1.stateChanged.connect(self.CS)
        
        self.opt2 = QtGui.QCheckBox("Whole words only",self)
        self.opt2.move(10,190)
        self.opt2.stateChanged.connect(self.WWO)

        self.close = QtGui.QPushButton("Close",self)
        self.close.move(270,220)
        self.close.clicked.connect(self.Close)
        
        
        self.setGeometry(300,300,360,250)

    def CS(self, state):
        global cs

        if state == QtCore.Qt.Checked:
            cs = True
        else:
            cs = False

    def WWO(self, state):
        global wwo
        print(wwo)

        if state == QtCore.Qt.Checked:
            wwo = True
        else:
            wwo = False

    def Close(self):
        self.hide()