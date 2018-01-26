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
from PyQt5.QtCore import QTextCodec
from PyQt5.QtCore import QIODevice
from PyQt5.QtCore import QByteArray
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QListWidgetItem
from TypoViewer.windows.mainWindow import Ui_MainWindow


# START
class iuniTools(QMainWindow):
    supportedFileFormats = ['docx']

    def __init__(self, parent=None):
        super(iuniTools, self).__init__(parent)
        self.createUi()

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

        #id = QFontDatabase.addApplicationFont(":/fonts/Ali-Uni_Samik_Regular.otf")
        #family = QFontDatabase.applicationFontFamilies(id)[0]
        #ali_samik = QFont(family)
        #self.ui.textEdit.setFont(ali_samik)
        #self.ui.textEdit.setFontPointSize(72)
        self.setAcceptDrops(True)
        self.ui.textEdit.setAcceptDrops(False)

        stream = QFile(":/samples/arabic_2.txt")
        if stream.open(QFile.ReadOnly):
            sampleText = str(stream.readAll(), 'utf-8')
            stream.close()
        else:
            print(stream.errorString())

        self.ui.textEdit.setText(sampleText)

        # self.ui.actionDeleteItems.triggered.connect(self.removeFromTable)
        # self.ui.actionClearList.triggered.connect(self.removeAllFromTable)
        # self.ui.actionSelectFiles.triggered.connect(self.selectSourceFileDialog)
        # self.ui.btnConvert.clicked.connect(self.doConvert)

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
                id = QFontDatabase.addApplicationFont(fileName)
                family = QFontDatabase.applicationFontFamilies(id)[0]
                font = QFont(family)
                self.ui.textEdit.setFont(font)
                self.ui.textEdit.setFontPointSize(72)
                print(fileName)
            event.accept()
        else:
            event.ignore()


app = QApplication([])
win = iuniTools()

win.show()

app.exec_()
