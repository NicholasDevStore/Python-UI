from qtpy.QtCore import Qt, QRect, QPoint, Signal
from qtpy.QtWidgets import QFrame, QLabel, QBoxLayout, QHBoxLayout
from qtpy.QtGui import QColor, QPainter, QPen, QPainterPath
from elidelabel import ElideLabel

class PCheck(QFrame):

    stateChanged = Signal(bool)

    x1 = QPoint(6, 16)
    x2 = QPoint(14, 24)
    x3 = QPoint(24, 9)

    def __init__(self, parent = None):
        super().__init__(parent)

        self.is_checked = False
        self.is_pressed = False

        self.border_radius = 0
        self.check_thick = 2
        self.back_color = QColor(108, 108, 115)
        self.check_color = QColor(255, 255, 255)

    def resizeEvent(self, event):

        self.border_radius = self.height() / 4
        self.update()

    def mousePressEvent(self, event):

        QFrame.mousePressEvent(self, event)

        self.is_pressed = True
        self.update()

    def mouseReleaseEvent(self, event):

        QFrame.mouseReleaseEvent(self, event)

        if self.is_pressed:
            self.is_checked = not self.is_checked
            self.stateChanged.emit(self.is_checked)

        self.is_pressed = False
        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        side = min(self.width(), self.height())
        painter.scale(side / 32.0, side / 32.0)

        painter.setPen(Qt.NoPen)

        if not self.is_pressed:
            painter.setBrush(self.back_color)
        else:
            painter.setBrush(QColor(self.back_color.red() + 30, self.back_color.green() + 30, self.back_color.blue() + 30))

        painter.drawRoundedRect(QRect(0, 0, 32, 32), 8, 8)

        if self.is_checked:

            check_path = QPainterPath()
            check_path.moveTo(self.x1)
            check_path.lineTo(self.x2)
            check_path.lineTo(self.x3)

            pen = QPen(self.check_color, self.check_thick, Qt.SolidLine)
            painter.setPen(pen)

            painter.drawPath(check_path)

class PCheckBox(QFrame):
    """ Customized check box """

    stateChanged = Signal(bool)

    def __init__(self, parent = None):
        super().__init__(parent)

        self.is_checked = False
        self.direction = 1 # 0: LeftToRight, 1: RightToLeft
        self.spacing = 5

        self.between = True

        self.label = ElideLabel(self)
        self.label.setObjectName("checkBoxText")
        self.check = PCheck(self)
        self.check.stateChanged.connect(self.stateChanged)

    def set_direction(self, direction_):

        self.direction = direction_

        if self.between:
            if self.direction == 0:
                self.label.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            elif self.direction == 1:
                self.label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)

        self.update_positions()

    def set_text_alignment(self, align):

        self.label.setAlignment(align)

    def set_text_font(self, font):

        self.label.setFont(font)

    def set_text_color(self, color):

        self.label.setStyleSheet(f"#checkBoxText {{color: rgb({color.red()}, {color.green()}, {color.blue()})}}")

    def set_text(self, text_):

        self.label.setText(text_)

    def text(self):

        return self.label.text()

    def update_positions(self):

        if self.direction == 0: # LeftToRight, checkbox on the left
            self.check.setGeometry(0, 0, self.height(), self.height())
            self.label.setGeometry(self.check.width() + self.spacing, 0, self.width() -  self.check.width() - 5,
                                   self.height())
        else:
            self.check.setGeometry(self.width() - self.height() - self.spacing, 0, self.height(), self.height())
            self.label.setGeometry(0, 0, self.width() - self.check.width() - 5,
                                   self.height())

    def resizeEvent(self, event):

        QFrame.resizeEvent(self, event)

        self.update_positions()
        font = self.label.font()
        font.setPointSize(self.height() / 2)
        self.label.setFont(font)


if __name__ == "__main__":

    from qtpy.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout

    app = QApplication()

    w = QWidget()
    w.setGeometry(100, 100, 300, 300)

    layout = QHBoxLayout(w)

    check = PCheckBox(w)
    check.set_text("Full Address Only")
    check.set_direction(QBoxLayout.LeftToRight)
    check.set_text_color(QColor(255, 255, 255))

    layout.addWidget(check)

    w.show()

    app.exec_()
