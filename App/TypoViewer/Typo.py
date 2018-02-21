# -*- coding: utf-8 -*-
# fadox.net <fadox@gmx.net>
# created: 25.01.2018

from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtGui import QTextCursor
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QFile, QSize, QPoint
from PyQt5.QtCore import Qt, QSizeF

from PyQt5.QtCore import QFileSystemWatcher
from PyQt5.QtCore import QTextCodec
from PyQt5.QtCore import QIODevice
from PyQt5.QtCore import QByteArray
from PyQt5.Qt import QPrinter
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QListWidgetItem
from TypoViewer.windows.mainWindow import Ui_MainWindow
from TypoViewer.objects.settings import TypoSettings
from TypoViewer.objects.usertexts import UserTexts
from PyQt5.QtCore import QSignalBlocker
import os


# START
class MainApp(QMainWindow):
    supportedFileFormats = ['docx']

    def __init__(self, parent=None):
        self.settings = TypoSettings().getSettings()
        self.user_texts = UserTexts().getTexts()
        self.text_style = {'background-color':'#FFFEEE', 'font-size':'28pt'}
        #os.environ['QT_HARFBUZZ'] = 'old'
        super(MainApp, self).__init__(parent)
        self.observer = QFileSystemWatcher()
        self.createUi()
        self.fontsDB = QFontDatabase()
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
        self.ui.setupUi(self)
        self.move(50, 50)
        self.setAcceptDrops(True)

        # transparent
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background: transparent; border: none;")
        self.oldPos = self.pos()



        # disable observe checkbox on start
        self.ui.chkObserve.setEnabled(False)

        self.setAcceptDrops(True)
        self.ui.textEdit.setAcceptDrops(False)

        self.ui.cmbTextSamples.currentIndexChanged.connect(self.setSampleText)
        self.ui.cmbFontSize.currentIndexChanged.connect(self.setFontSize)
        self.observer.fileChanged.connect(self.setTextFont)
        self.ui.textEdit.textChanged.connect(self.saveUserText)
        self.ui.btnPdbExport.clicked.connect(self.exportToPdf)


        #self.ui.textEdit

        self.resize(self.settings.value("size", QSize(270, 225)))
        self.move(self.settings.value("pos", QPoint(50, 50)))
        self.setCustomSampleText()
        self.refreshTextStyle()

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





    def setTextFont(self, fileName):
        #print(fileName)
        QFontDatabase.removeAllApplicationFonts()
        id = QFontDatabase.addApplicationFont(fileName)
        family = QFontDatabase.applicationFontFamilies(id)[0]
        font = QFontDatabase.font(self.fontsDB, family, 'bold', 48)
        font.setStrikeOut(False)
        #font.setStyleHint(QFont.SansSerif)
        #sysFont = QFontDatabase.font(self.fontsDB,'Lucida Grande UI','bold',300)
        self.ui.textEdit.setFont(font)
        self.ui.chkObserve.setEnabled(True)
        return family

    def setFontSize(self, index):
        fontSize = self.ui.cmbFontSize.itemText(index)
        try:
            self.text_style['font-size'] = fontSize + 'pt'
        except:
            print('error on set font size')
        self.refreshTextStyle()

    def refreshTextStyle(self):
        style = ""
        for prop in self.text_style.items():
            style += prop[0] + ": " + prop[1] + "; "
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
                fontName = self.setTextFont(fileName)
                if fontName:
                    self.setActiveFontLabel(fontName)
            event.accept()
        else:
            event.ignore()
    def closeEvent(self, e):
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        e.accept()

app = QApplication([])
#font= QFont("Courier New")
#font.setStyleHint(QFont.Monospace)
#app.setFont(font)
win = MainApp()

win.show()

app.exec_()
