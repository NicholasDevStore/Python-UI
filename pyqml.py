import os, sys
import PySide2.QtQml
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl, Signal
from PySide2.QtGui import QGuiApplication
import getpass
from datetime import datetime
import re

def cleanup(string):
    
    return re.sub(r'\W+', '_', string)

def saveCredential(cre, title, url, email, username, password, notes):

    # basepath = '/path/to/encrypted/volume'
    basepath = '/Volumes/PRO'
 
    mytimestamp = cleanup( datetime.today().strftime('%Y-%m-%d-%H:%M:%S') )
    fullpath = basepath + "/" + cre + "/" + cleanup(title) + "_" + mytimestamp + ".txt"

    sharedby = getpass.getuser()

    output_text = "[Title:]\t%s\n[Shared by:]\t%s\n[URL:]\t\t%s\n[Accnt email:]\t%s\n[Username:]\t%s\n[Password:]\t%s\n[Notes:]\n%s\n[Date:]\t%s\n" % (title, sharedby, url, email, username, password, notes, mytimestamp)

    output_file = open(fullpath, 'w')
    output_file.write(output_text)
    output_file.close()

    root.showMessageDialog()

if __name__ == '__main__':

    #Set up the application window
    app = QGuiApplication(sys.argv)
    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)

    #Load the QML file
    qml_file = os.path.join(os.path.dirname(__file__),"view.qml")
    view.setSource(QUrl.fromLocalFile(os.path.abspath(qml_file)))

    global root
    root = view.rootObject()

    root.close_clicked.connect(app.exit)
    root.save_clicked.connect(saveCredential)

    #Show the window
    if view.status() == QQuickView.Error:
        sys.exit(-1)
    view.show()

    #execute and cleanup
    app.exec_()
    del view