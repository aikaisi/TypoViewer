# -*- coding: utf-8 -*-
# fadox.net <fadox@gmx.net>
# created: 25.01.2018

from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QFile
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QFileSystemWatcher
from PyQt5.QtCore import QTextCodec
from PyQt5.QtCore import QIODevice
from PyQt5.QtCore import QByteArray
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QListWidgetItem
from TypoViewer.windows.mainWindow import Ui_MainWindow
import os


# START
class iuniTools(QMainWindow):
    supportedFileFormats = ['docx']

    def __init__(self, parent=None):
        self.text_style = {'background-color':'#FFFEEE', 'font-size':'72pt'}
        os.environ['QT_HARFBUZZ'] = 'old'
        super(iuniTools, self).__init__(parent)
        self.observer = QFileSystemWatcher()
        self.createUi()
        self.fontsDB = QFontDatabase()


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
        self.setStyleSheet("background: transparent; border: none;")

        #self.ui.textEdit.setFontPointSize(122)
        #self.ui.textEdit.setStyleSheet('line-height: 10px;background-color:#ffffff;')
        #high = self.ui.textEdit.document().size().height()

        # disable observe checkbox on start
        self.ui.chkObserve.setEnabled(False)

        self.setAcceptDrops(True)
        self.ui.textEdit.setAcceptDrops(False)

        self.ui.cmbTextSamples.currentIndexChanged.connect(self.setSampleText)
        self.ui.cmbFontSize.currentIndexChanged.connect(self.setFontSize)
        self.observer.fileChanged.connect(self.setTextFont)
        self.refreshTextStyle()


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


    def setCustomSampleText(self):
        self.ui.textEdit.setText("Hallo World")
        return True


    def setTextFont(self, fileName):
        print(fileName)
        QFontDatabase.removeAllApplicationFonts()
        id = QFontDatabase.addApplicationFont(fileName)
        family = QFontDatabase.applicationFontFamilies(id)[0]
        font = QFontDatabase.font(self.fontsDB, family, 'bold', 128)
        font.setStrikeOut(False)
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


app = QApplication([])
win = iuniTools()

win.show()

app.exec_()
