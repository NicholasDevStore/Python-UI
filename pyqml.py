import os, sys
import PySide2.QtQml
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl
from PySide2.QtGui import QGuiApplication

if __name__ == '__main__':

    #Set up the application window
    app = QGuiApplication(sys.argv)
    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)

    #Load the QML file
    qml_file = os.path.join(os.path.dirname(__file__),"view.qml")
    view.setSource(QUrl.fromLocalFile(os.path.abspath(qml_file)))

    #Show the window
    if view.status() == QQuickView.Error:
        sys.exit(-1)
    view.show()

    #execute and cleanup
    app.exec_()
    del view