# -*- coding: utf-8 -*-
# fadox.net <fadox@gmx.net>
# created: 25.01.2018

from PyQt5.QtCore import QSettings

class TypoSettings:
    def __init__(self):
        self.settings = QSettings(QSettings.IniFormat, QSettings.SystemScope, 'TypoViewer', 'typo')
        #self.settings = QSettings('settings.ini', QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)  # File only, not registry or or.
        print (self.settings.fileName())

    def getSettings(self):
        return self.settings
