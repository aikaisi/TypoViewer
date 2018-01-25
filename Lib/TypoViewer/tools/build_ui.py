# -*- coding: utf-8 -*-

# build_ui.py
#
# this script automate the converting of layout files made with
# Qt Designer to the equivalent Python layout format
#
# fadox.net <fadox@gmx.net>
# created: 25.01.2018

import os
import sys
import time
from tempfile import mkstemp
from os import close
from shutil import move


def main():
    # Windows OS
    if os.name == 'nt':
        envPath = (os.sep).join(sys.executable.split(os.sep)[:-1])

        makeResources = "\pyrcc5.exe -o ../resources/icons_db.py ../resources/icons_db.qrc"
        makeLayout = "\pyuic5.exe -o ../windows/mainWindow.py ../windows/mainWindow.ui"
    # OSX
    else:
        envPath = ""
        makeResources = "pyside-rcc -o layout_rc.py ui/layout.qrc"
        makeLayout = "pyside-uic -o mainwindow_ui.py ui/mainWindow.ui"

    # Convert *layout* resources file (qrc) to *layout*_ui.py
    os.system(envPath + makeResources)

    # Convert Qt Main *Window* file (ui) to *window'_ui.py
    os.system(envPath + makeLayout)

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)

    #Remove original file
    #remove(file_path)
    #Move new file
    move(abs_path, file_path)

def addDilimeters():
    #replace('../layout_rc.py','qt_resource_data',"# START\nqt_resource_data")
    #replace('../mainwindow_ui.py','class Ui_MainWindow',"# START\nclass Ui_MainWindow")
    replace('../windows/mainWindow.py','import icons_db_rc',"import TypoViewer.resources.icons_db")

if __name__ == '__main__':
    main()
    time.sleep(3)
    addDilimeters()
