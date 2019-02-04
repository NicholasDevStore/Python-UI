from qtpy.QtCore import Qt
from qtpy.QtWidgets import QLabel
from qtpy.QtGui import QColor

class PLabel(QLabel):
    """ Handle widget for range slider """

    def __init__(self, parent = None):
        super().__init__(parent)

        self.backColor = QColor(108, 108, 115)
        self.borderRadius = 0
        self.textColor = QColor(255, 255, 255)

        self.qssString = ""

        self.setObjectName("plabel")
        self.update_stylesheet()
        self.setAlignment(Qt.AlignCenter)

    def update_stylesheet(self):
        """
        create QSS with self properties and apply style

        :param self:
        :return:
        """

        self.qssString = f"#plabel {{background: rgb({self.backColor.red()}, {self.backColor.green()}, {self.backColor.blue()});" \
                         f"color: rgb({self.textColor.red()}, {self.textColor.green()}, {self.textColor.blue()});" \
                         f"border-radius: {self.borderRadius}}}"

        self.setStyleSheet(self.qssString)

    def resizeEvent(self, event):

        QLabel.resizeEvent(self, event)

        self.borderRadius = self.height() / 4
        self.update_stylesheet()
