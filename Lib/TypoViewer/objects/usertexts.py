# -*- coding: utf-8 -*-
# fadox.net <fadox@gmx.net>
# created: 25.01.2018

from PyQt5.QtCore import QSettings

class UserTexts:
    def __init__(self):
        self.texts = QSettings(QSettings.IniFormat, QSettings.SystemScope, 'TypoViewer', 'user')
        #self.settings = QSettings('settings.ini', QSettings.IniFormat)
        self.texts.setFallbacksEnabled(False)  # File only, not registry or or.
        self.texts.setValue('xx','yyyy')

    def getTexts(self):
        return self.texts
