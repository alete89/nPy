import sys
import time
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

var = 0
f = ""
choiceStr = ""
cs = False
wwo = False

tt = True
tf = True
ts = True


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

class Date(QtGui.QDialog):
    def __init__(self,parent = None):
        QtGui.QDialog.__init__(self, parent)
        
        self.initUI()

    def initUI(self):

        self.form = QtGui.QComboBox(self)
        self.form.move(10,10)
        self.form.addItem(time.strftime("%d.%m.%Y"))
        self.form.addItem(time.strftime("%A, %d. %B %Y"))
        self.form.addItem(time.strftime("%d. %B %Y"))
        self.form.addItem(time.strftime("%d %m %Y"))
        self.form.addItem(time.strftime("%X"))
        self.form.addItem(time.strftime("%x"))
        self.form.addItem(time.strftime("%H:%M"))
        self.form.addItem(time.strftime("%A, %d. %B %Y %H:%M"))
        self.form.addItem(time.strftime("%d.%m.%Y %H:%M"))
        self.form.addItem(time.strftime("%d. %B %Y %H:%M"))

        self.form.activated[str].connect(self.handleChoice)
        
        self.ok = QtGui.QPushButton("Insert",self)
        self.ok.move(180,10)

        self.cancel = QtGui.QPushButton("Cancel",self)
        self.cancel.move(180,40)
        self.cancel.clicked.connect(self.Cancel)

        self.setGeometry(300,300,280,70)

    def handleChoice(self,choice):
        global choiceStr

        choiceStr = choice

        print(choiceStr)

    def Cancel(self):
        self.close()
        
class Main(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self,None)
        self.initUI()

    def initUI(self):

#------- Toolbar --------------------------------------

#-- Upper Toolbar -- 

        newAction = QtGui.QAction(QtGui.QIcon("icons/new.png"),"New",self)
        newAction.setShortcut("Ctrl+N")
        newAction.setStatusTip("Create a new document from scratch.")
        newAction.triggered.connect(self.New)

        openAction = QtGui.QAction(QtGui.QIcon("icons/open.png"),"Open file",self)
        openAction.setStatusTip("Open existing document")
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.Open)

        saveAction = QtGui.QAction(QtGui.QIcon("icons/save.png"),"Save",self)
        saveAction.setStatusTip("Save document")
        saveAction.setShortcut("Ctrl+S")
        saveAction.triggered.connect(self.Save)

        previewAction = QtGui.QAction(QtGui.QIcon("icons/preview.png"),"Page view",self)
        previewAction.setStatusTip("Preview page before printing")
        previewAction.setShortcut("Ctrl+Shift+P")
        previewAction.triggered.connect(self.PageView)

        findAction = QtGui.QAction(QtGui.QIcon("icons/find.png"),"Find",self)
        findAction.setStatusTip("Find words in your document")
        findAction.setShortcut("Ctrl+F")
        findAction.triggered.connect(self.Find)

        cutAction = QtGui.QAction(QtGui.QIcon("icons/cut.png"),"Cut to clipboard",self)
        cutAction.setStatusTip("Delete and copy text to clipboard")
        cutAction.setShortcut("Ctrl+X")
        cutAction.triggered.connect(self.Cut)

        copyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"),"Copy to clipboard",self)
        copyAction.setStatusTip("Copy text to clipboard")
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(self.Copy)

        pasteAction = QtGui.QAction(QtGui.QIcon("icons/paste.png"),"Paste from clipboard",self)
        pasteAction.setStatusTip("Paste text from clipboard")
        pasteAction.setShortcut("Ctrl+V")
        pasteAction.triggered.connect(self.Paste)

        undoAction = QtGui.QAction(QtGui.QIcon("icons/undo.png"),"Undo last action",self)
        undoAction.setStatusTip("Undo last action")
        undoAction.setShortcut("Ctrl+Z")
        undoAction.triggered.connect(self.Undo)

        redoAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"),"Redo last undone thing",self)
        redoAction.setStatusTip("Redo last undone thing")
        redoAction.setShortcut("Ctrl+Y")
        redoAction.triggered.connect(self.Redo)

        dtAction = QtGui.QAction(QtGui.QIcon("icons/datetime.png"),"Insert current date/time",self)
        dtAction.setStatusTip("Insert current date/time")
        dtAction.setShortcut("Ctrl+D")
        dtAction.triggered.connect(self.DateTime)

        printAction = QtGui.QAction(QtGui.QIcon("icons/print.png"),"Print document",self)
        printAction.setStatusTip("Print document")
        printAction.setShortcut("Ctrl+P")
        printAction.triggered.connect(self.Print)

        self.toolbar = self.addToolBar("Options")
        self.toolbar.addAction(newAction)
        self.toolbar.addAction(openAction)
        self.toolbar.addAction(saveAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(printAction)
        #self.toolbar.addAction(pdfAction)
        self.toolbar.addAction(previewAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(findAction)
        self.toolbar.addAction(cutAction)
        self.toolbar.addAction(copyAction)
        self.toolbar.addAction(pasteAction)
        self.toolbar.addAction(undoAction)
        self.toolbar.addAction(redoAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(dtAction)
        self.toolbar.addSeparator()

        self.addToolBarBreak()

# -- Lower Toolbar -- 

        self.fontFamily = QtGui.QFontComboBox(self)
        self.fontFamily.currentFontChanged.connect(self.FontFamily)

        fontSize = QtGui.QComboBox(self)
        fontSize.setEditable(True)
        fontSize.setMinimumContentsLength(3)
        fontSize.activated.connect(self.FontSize)
        flist = [6,7,8,9,10,11,12,13,14,15,16,18,20,22,24,26,28,32,36,40,44,48,
                 54,60,66,72,80,88,96]
        
        for i in flist:
            fontSize.addItem(str(i))

        fontColor = QtGui.QAction(QtGui.QIcon("icons/color.png"),"Change font color",self)
        fontColor.triggered.connect(self.FontColor)

        boldAction = QtGui.QAction(QtGui.QIcon("icons/bold.png"),"Bold",self)
        boldAction.triggered.connect(self.Bold)
        
        italicAction = QtGui.QAction(QtGui.QIcon("icons/italic.png"),"Italic",self)
        italicAction.triggered.connect(self.Italic)
        
        underlAction = QtGui.QAction(QtGui.QIcon("icons/underl.png"),"Underline",self)
        underlAction.triggered.connect(self.Underl)

        alignLeft = QtGui.QAction(QtGui.QIcon("icons/alignLeft.png"),"Align left",self)
        alignLeft.triggered.connect(self.alignLeft)

        alignCenter = QtGui.QAction(QtGui.QIcon("icons/alignCenter.png"),"Align center",self)
        alignCenter.triggered.connect(self.alignCenter)

        alignRight = QtGui.QAction(QtGui.QIcon("icons/alignRight.png"),"Align right",self)
        alignRight.triggered.connect(self.alignRight)

        alignJustify = QtGui.QAction(QtGui.QIcon("icons/alignJustify.png"),"Align justify",self)
        alignJustify.triggered.connect(self.alignJustify)

        indentAction = QtGui.QAction(QtGui.QIcon("icons/indent.png"),"Indent Area",self)
        indentAction.setShortcut("Ctrl+Tab")
        indentAction.triggered.connect(self.Indent)

        dedentAction = QtGui.QAction(QtGui.QIcon("icons/dedent.png"),"Dedent Area",self)
        dedentAction.setShortcut("Shift+Tab")
        dedentAction.triggered.connect(self.Dedent)

        backColor = QtGui.QAction(QtGui.QIcon("icons/backcolor.png"),"Change background color",self)
        backColor.triggered.connect(self.FontBackColor)

        bulletAction = QtGui.QAction(QtGui.QIcon("icons/bullet.png"),"Insert Bullet List",self)
        bulletAction.triggered.connect(self.BulletList)

        numberedAction = QtGui.QAction(QtGui.QIcon("icons/number.png"),"Insert Numbered List",self)
        numberedAction.triggered.connect(self.NumberedList)

        space1 = QtGui.QLabel("  ",self)
        space2 = QtGui.QLabel(" ",self)
        space3 = QtGui.QLabel(" ",self)
        

        self.formatbar = self.addToolBar("Format")
        self.formatbar.addWidget(self.fontFamily)
        self.formatbar.addWidget(space1)
        self.formatbar.addWidget(fontSize)
        self.formatbar.addWidget(space2)
        
        self.formatbar.addSeparator()

        self.formatbar.addAction(fontColor)
        self.formatbar.addAction(backColor)

        self.formatbar.addSeparator()
        
        self.formatbar.addAction(boldAction)
        self.formatbar.addAction(italicAction)
        self.formatbar.addAction(underlAction)
        
        self.formatbar.addSeparator()

        self.formatbar.addAction(alignLeft)
        self.formatbar.addAction(alignCenter)
        self.formatbar.addAction(alignRight)
        self.formatbar.addAction(alignJustify)

        self.formatbar.addSeparator()

        self.formatbar.addAction(indentAction)
        self.formatbar.addAction(dedentAction)
        self.formatbar.addAction(bulletAction)
        self.formatbar.addAction(numberedAction)
        
#------- Text Edit -----------------------------------

        self.text = QtGui.QTextEdit(self)
        self.text.setTabStopWidth(12)
        self.setCentralWidget(self.text)

#------- Statusbar ------------------------------------
        
        self.status = self.statusBar()

        self.text.cursorPositionChanged.connect(self.CursorPosition)


#---------Window settings --------------------------------
        
        self.setGeometry(100,100,700,700)
        self.setWindowTitle("Scriber")
        self.setWindowIcon(QtGui.QIcon("icons/feather.png"))
        self.show()

#------- Menubar --------------------------------------
        
        menubar = self.menuBar()
        file = menubar.addMenu("File")
        edit = menubar.addMenu("Edit")
        view = menubar.addMenu("View")

        file.addAction(newAction)
        file.addAction(openAction)
        file.addAction(saveAction)
        file.addAction(printAction)
        file.addAction(previewAction)

        edit.addAction(undoAction)
        edit.addAction(redoAction)
        edit.addAction(cutAction)
        edit.addAction(copyAction)
        edit.addAction(findAction)
        edit.addAction(dtAction)

        toggleTool = QtGui.QAction("Toggle Toolbar",self,checkable=True)
        toggleTool.triggered.connect(self.handleToggleTool)
        
        toggleFormat = QtGui.QAction("Toggle Formatbar",self,checkable=True)
        toggleFormat.triggered.connect(self.handleToggleFormat)
        
        toggleStatus = QtGui.QAction("Toggle Statusbar",self,checkable=True)
        toggleStatus.triggered.connect(self.handleToggleStatus)

        view.addAction(toggleTool)
        view.addAction(toggleFormat)
        view.addAction(toggleStatus)

    def handleToggleTool(self):
        global tt

        if tt == True:
            self.toolbar.hide()
            tt = False
        else:
            self.toolbar.show()
            tt = True

    def handleToggleFormat(self):
        global tf

        if tf == True:
            self.formatbar.hide()
            tf = False
        else:
            self.formatbar.show()
            tf = True

    def handleToggleStatus(self):
        global ts

        if ts == True:
            self.status.hide()
            ts = False
        else:
            self.status.show()
            ts = True
            
#-------- Toolbar slots -----------------------------------

    def New(self):
        self.text.clear()

    def Open(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        f = open(filename, 'r')
        filedata = f.read()
        self.text.setText(filedata)
        f.close()

    def Save(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        f = open(filename, 'w')
        filedata = self.text.toPlainText()
        f.write(filedata)
        f.close()

    def PageView(self):
        preview = QtGui.QPrintPreviewDialog()
        preview.paintRequested.connect(self.PaintPageView)
        preview.exec_()

    def Print(self):
        dialog = QtGui.QPrintDialog()
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.text.document().print_(dialog.printer())

    def PDF(self):
        printer = QtGui.QPrinter()
        printer.setOutputFormat(printer.NativeFormat)
        
        dialog = QtGui.QPrintDialog(printer)
        dialog.setOption(dialog.PrintToFile)
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.text.document().print_(dialog.printer())
        
        
    def PaintPageView(self, printer):
        self.text.print_(printer)

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
            
            self.text.find(f,flag or 0)

        def handleReplace():
            f = find.te.toPlainText()
            r = find.rp.toPlainText()

            text = self.text.toPlainText()
            
            newText = text.replace(f,r)

            self.text.clear()
            self.text.append(newText)
        
        find.src.clicked.connect(handleFind)
        find.rpb.clicked.connect(handleReplace)


    def Undo(self):
        self.text.undo()

    def Redo(self):
        self.text.redo()

    def Cut(self):
        self.text.cut()

    def Copy(self):
        self.text.copy()

    def Paste(self):
        self.text.paste()

    def DateTime(self):

        date = Date(self)
        date.show()

        date.ok.clicked.connect(self.insertDate)

    def insertDate(self):
        global choiceStr
        print(choiceStr)
        self.text.append(choiceStr)
        
    def CursorPosition(self):
        line = self.text.textCursor().blockNumber()
        col = self.text.textCursor().columnNumber()
        linecol = ("Line: "+str(line)+" | "+"Column: "+str(col))
        self.status.showMessage(linecol)

    def FontFamily(self,font):
        font = QtGui.QFont(self.fontFamily.currentFont())
        self.text.setCurrentFont(font)

    def FontSize(self, fsize):

        size = (int(fsize))
        self.text.setFontPointSize(size)

    def FontColor(self):
        c = QtGui.QColorDialog.getColor()

        self.text.setTextColor(c)
        
    def FontBackColor(self):
        c = QtGui.QColorDialog.getColor()

        self.text.setTextBackgroundColor(c)

    def Bold(self):
        w = self.text.fontWeight()
        if w == 50:
            self.text.setFontWeight(QtGui.QFont.Bold)
        elif w == 75:
            self.text.setFontWeight(QtGui.QFont.Normal)
        
    def Italic(self):
        i = self.text.fontItalic()
        
        if i == False:
            self.text.setFontItalic(True)
        elif i == True:
            self.text.setFontItalic(False)
        
    def Underl(self):
        ul = self.text.fontUnderline()

        if ul == False:
            self.text.setFontUnderline(True) 
        elif ul == True:
            self.text.setFontUnderline(False)
            
    def lThrough(self):
        lt = QtGui.QFont.style()

        print(lt)

    def alignLeft(self):
        self.text.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        self.text.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        self.text.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        self.text.setAlignment(Qt.AlignJustify)

    def Indent(self):
        tab = "\t"
        cursor = self.text.textCursor()

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.setPosition(end)
        cursor.movePosition(cursor.EndOfLine)
        end = cursor.position()

        cursor.setPosition(start)
        cursor.movePosition(cursor.StartOfLine)
        start = cursor.position()


        while cursor.position() < end:
            global var

            print(cursor.position(),end)
            
            cursor.movePosition(cursor.StartOfLine)
            cursor.insertText(tab)
            cursor.movePosition(cursor.Down)
            end += len(tab)

            '''if cursor.position() == end:
                var +=1

            if var == 2:
                break'''
            
            

    def Dedent(self):
        tab = "\t"
        cursor = self.text.textCursor()

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.setPosition(end)
        cursor.movePosition(cursor.EndOfLine)
        end = cursor.position()

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

    def BulletList(self):
        print("bullet connects!")
        self.text.insertHtml("<ul><li> ...</li></ul>")

    def NumberedList(self):
        print("numbered connects!")
        self.text.insertHtml("<ol><li> ...</li></ol>")
         
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()