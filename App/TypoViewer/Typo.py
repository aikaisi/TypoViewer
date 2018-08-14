# -*- coding: utf-8 -*-
# fadox.net <fadox@gmx.net>
# created: 25.01.2018

from PySide2.QtGui import QIcon
from PySide2.QtGui import QColor
from PySide2.QtGui import QPixmap
from PySide2.QtGui import QFontDatabase
from PySide2.QtGui import QTextCharFormat
from PySide2.QtGui import QTextCursor
from PySide2.QtGui import QFont
from PySide2.QtCore import QFile, QSize, QPoint
from PySide2.QtCore import Qt, QSizeF

from PySide2.QtCore import QFileSystemWatcher
from PySide2.QtCore import QTextCodec
from PySide2.QtCore import QIODevice
from PySide2.QtCore import QByteArray
from PySide2.QtPrintSupport import QPrinter
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QListWidgetItem
from PySide2.QtWidgets import QSizeGrip
from TypoViewer.windows.mainWindow import Ui_MainWindow
from TypoViewer.objects.settings import TypoSettings
from TypoViewer.objects.usertexts import UserTexts
from PySide2.QtCore import QSignalBlocker
import os, random


# START
class MainApp(QMainWindow):

    supportedFileFormats = ['docx']

    def __init__(self, parent=None):
        self.settings = TypoSettings().getSettings()
        self.user_texts = UserTexts().getTexts()

        self.text_font_size = "128"
        #self.text_background_color = "#FFFEEE"
        self.text_color = "#FF0000"

        #os.environ['QT_HARFBUZZ'] = 'old'
        super(MainApp, self).__init__(parent)
        self.observer = QFileSystemWatcher()
        self.createUi()

        self.userTextIds = [0]



    def convertToUnicode(self, source, target):
        """
        wordFile = KuConv.load(source, 'Word2007')
        convertedFile = KuConv.convert(wordFile, 'Word2007')
        isConverted = KuConv.write(convertedFile, target,'Word2007')
        return isConverted
        """
        pass

    def addToQueue(self, fileName):
        if fileName:
            info = self.getFileInfo(fileName)
            if info['typ'] in self.supportedFileFormats:
                tmpIndex = self.exisstInTable(info)
                if tmpIndex is not None:
                    self.setListItemStatus(tmpIndex, '0')
                else:
                    self.addToTable(info)

    def setListItemStatus(self, index, value):
        row = self.ui.listWidget.item(index)
        data = row.data(Qt.UserRole)
        data['status'] = value
        color = QColor(Qt.green)
        color.setAlpha(int(value) / 2)
        row.setData(Qt.BackgroundRole, color)
        row.setData(Qt.UserRole, data)

    def addToTable(self, fileData):
        nameColumn = QListWidgetItem(fileData['fileName'])
        iconPath = ':/icons/' + fileData['typ'] + '.png'
        itemIcon = QIcon()
        itemIcon.addPixmap(QPixmap(iconPath), QIcon.Normal, QIcon.Off)
        nameColumn.setIcon(itemIcon)
        fileData['status'] = '0'
        nameColumn.setData(Qt.UserRole, fileData)

        color = QColor(Qt.green)
        color.setAlpha(int(fileData['status']))
        nameColumn.setData(Qt.BackgroundRole, color)

        self.ui.listWidget.addItem(nameColumn)

    def exisstInTable(self, info):
        filesCount = self.ui.listWidget.count()
        for index in range(filesCount):
            row = self.ui.listWidget.item(index)
            data = row.data(Qt.UserRole)
            if data['fileName'] == info['fileName']:
                if data['path'] == info['path']:
                    return index

    def createUi(self):
        self.ui = Ui_MainWindow()
        self.fontsDB = QFontDatabase()
        self.ui.setupUi(self)
        self.move(50, 50)
        self.setAcceptDrops(True)
        self.last_font = None

        # transparent
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        self.setStyleSheet("background: transparent; border: none;")
        self.oldPos = self.pos()

        seizGrip = QSizeGrip(self)
        self.ui.sldTrans.setValue(99)
        self.text_background_color = "#333333"
        #self.text_background_color = "transparent"
        self.text_color = "#FFFEEE"




        # disable observe checkbox on start
        self.ui.chkObserve.setEnabled(False)

        self.setAcceptDrops(True)
        self.ui.textEdit.setAcceptDrops(False)

        self.ui.cmbTextSamples.currentIndexChanged.connect(self.setSampleText)
        self.ui.cmbFontSize.currentIndexChanged.connect(self.setFontSize)
        self.observer.fileChanged.connect(self.setTextFont)
        self.ui.textEdit.textChanged.connect(self.saveUserText)
        self.ui.btnPdbExport.clicked.connect(self.exportToPdf)
        self.ui.sldTrans.valueChanged.connect(self.adjustTransparent)


        #self.ui.textEdit




        self.resize(self.settings.value("size", QSize(270, 225)))
        self.move(self.settings.value("pos", QPoint(50, 50)))
        self.setCustomSampleText()
        self.refreshTextStyle()
        try:
            self.text_font_size = self.settings.value("last_font_size", self.text_font_size)
            self.last_font = self.settings.value("last_font")
            if self.last_font:
                #self.setTextFont(self.last_font, int(self.text_font_size))
                pass
        except:
            pass

    def adjustTransparent(self,e):
        self.setWindowOpacity(e/100.0)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def exportToPdf(self):
        printer = QPrinter(QPrinter.PrinterResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setPaperSize(QPrinter.A4)
        printer.setOutputFileName('export_sample.pdf')
        document = self.ui.textEdit.document()
        size = QSizeF(printer.paperRect().size())
        document.setPageSize(size)
        document.print(printer)
        print('###')

    def getSelectedSampleTextId(self):
        selected = self.ui.cmbTextSamples.currentIndex()
        #print(selected)
        return selected


    def saveUserText(self):
        blocker = QSignalBlocker(self.ui.textEdit)
        selected = self.getSelectedSampleTextId()
        if selected in self.userTextIds:
            self.user_texts.setValue("text" + str(selected), self.ui.textEdit.toPlainText())
        m = 1


    def setCustomSampleText(self, id = 0):
        blocker = QSignalBlocker(self.ui.textEdit)
        vals = self.user_texts.value('text'+str(id), 'Write your Text here ..')
        self.ui.textEdit.setText(vals)
        return True

    def setSampleText(self, index):
        if index == 0:
            self.setCustomSampleText()
            return True
        try:
            sample_name = self.ui.cmbTextSamples.itemText(index)
            stream = QFile(":/samples/"+ sample_name +".txt")
            if stream.open(QFile.ReadOnly):
                sample_text = str(stream.readAll(), 'utf-8')
                stream.close()
            else:
                print(stream.errorString())

            self.ui.textEdit.setText(sample_text)
        except:
            print("error on opining sample text resource file")

        self.refreshTextStyle()
        """
        begin = 1
        end = 1000

        
        fmt = QTextCharFormat()
        fmt.setFontUnderline(True)
        fmt.setUnderlineStyle(QTextCharFormat.WaveUnderline)
        fmt.setUnderlineColor(Qt.red)

        cursor = QTextCursor(self.ui.textEdit.document())
        cursor.movePosition(QTextCursor.Start)

        for i in range (1, 100):
            cursor.movePosition(QTextCursor.StartOfWord)
            cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
            print()
            print('###')
            print(cursor.selectedText())
            cursor.setCharFormat(fmt)
            ff = cursor.charFormat().font()
            h = cursor.charFormat().font().StyleHint
            hh = cursor.charFormat().font().StyleHint()


            print(cursor.charFormat().font().family())
            print(cursor.charFormat().font().defaultFamily())

            cursor.movePosition(QTextCursor.NextWord, QTextCursor.MoveAnchor)
"""





    def setTextFont(self, fileName, size=92):
        print(size)

        bin = self.readFontFileAsBinary(fileName)
        QFontDatabase.removeAllApplicationFonts()
        #id = QFontDatabase.addApplicationFont(fileName)
        id = QFontDatabase.addApplicationFontFromData(bin)
        try:
            family = QFontDatabase.applicationFontFamilies(id)[0]
        except:
            return "Not found"
        font = QFontDatabase.font(self.fontsDB, family, 'bold', size)
        font.setStrikeOut(False)
        self.ui.textEdit.setFont(font)
        self.ui.textEdit.setCurrentFont(font)
        self.ui.chkObserve.setEnabled(True)
        return family

    def readFontFileAsBinary(self, path):
        f = QFile(path)
        f.open(QIODevice.ReadOnly | QIODevice.Unbuffered)

        try:
            content = f.readAll()
        finally:
            f.close()
        return content

    def setFontSize(self, index):
        fontSize = self.ui.cmbFontSize.itemText(index)
        self.text_font_size = fontSize
        if self.last_font:
            #self.setTextFont(self.last_font, int(fontSize))
            self.ui.textEdit.font().setPointSize(int(fontSize))

        self.refreshTextStyle()


    def refreshTextStyle(self):
        style = "background-color:%s;color:%s;font-size:%spt;" %\
                (self.text_background_color,self.text_color,self.text_font_size)
        print(style)
        self.ui.textEdit.setStyleSheet(style)

    def setActiveFontLabel(self, fontName):
        self.ui.lblActiveFont.setText(fontName)
        return True

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                fileName = url.toLocalFile()
                self.observer.addPath(fileName)
                self.last_font = fileName
                fontName = self.setTextFont(fileName)
                if fontName:
                    self.setActiveFontLabel(fontName)
            event.accept()
        else:
            event.ignore()
    def closeEvent(self, e):
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("last_font", self.last_font)
        self.settings.setValue("last_font_size", self.text_font_size)
        e.accept()

app = QApplication([])
#font= QFont("Courier New")
#font.setStyleHint(QFont.Monospace)
#app.setFont(font)

from PySide2.QtWidgets import QStyleFactory
app.setStyle(QStyleFactory.create('Fusion'))
win = MainApp()

win.show()

app.exec_()
