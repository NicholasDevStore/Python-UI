from qtpy.QtCore import Qt, QRect, QPoint, QPointF, Signal, QPropertyAnimation
from qtpy.QtWidgets import QFrame, QLabel, QBoxLayout, QHBoxLayout, QWidget, QListWidget, QComboBox, QSpinBox, QLineEdit
from qtpy.QtGui import QColor, QPainter, QPen, QPainterPath, QPainterPath, QFont, QPalette, QBrush, QPixmap, QValidator, QIntValidator, QPolygon
from pcombobox import PComboBox

class PLineEdit(QLineEdit):

    focusOut = Signal()

    def __init__(self, parent = None):

        super().__init__(parent)
        self.setObjectName("PLineEdit")
        self.back_color = QColor(108, 108, 115)
        self.text_color = QColor(255, 255, 255)
        self.set_style()

    def set_style(self):

        self.setStyleSheet(
            f"#PLineEdit {{background: rgba({self.back_color.red()}, {self.back_color.green()}, {self.back_color.blue()}, 255); "
            f"border: none; color: rgb({self.text_color.red()}, {self.text_color.green()}, {self.text_color.blue()});}}")

    def set_back_color(self, color):

        self.back_color = color
        self.set_style()

    def set_text_color(self, color):

        self.text_color = color
        self.set_style()

    def focusOutEvent(self, event):

        QLineEdit.focusOutEvent(self, event)
        self.focusOut.emit()

    def keyPressEvent(self, event):
        tmp = self.text()
        QLineEdit.keyPressEvent(self, event)

        if self.text() == "" or self.text() == "+":
            return

        value = int(self.text())
        if value > self.validator().top():
            print("Invalid!")
            self.setText(tmp)            
        

class PSpinBox(QFrame):

    valueChanged = Signal(int)

    def __init__(self, parent = None):

        super().__init__(parent)
        self.minimum = 0
        self.maximum = 100
        self.parent = parent
        self.value = 0
        self.singleStep = 1
        self.hover = False
        self.border_radius = 8
        self.rate = 0.25
        self.up_arrow_poly = QPolygon()
        self.down_arrow_poly = QPolygon()
        self.back_color = QColor(108, 108, 115)
        self.text_color = QColor(255, 255, 255)
        self.arrow_activate_color = QColor(255, 255, 255)
        self.arrow_deactivate_color = QColor(200, 200, 200)
        self.up_arrow_color = self.arrow_deactivate_color
        self.down_arrow_color = self.arrow_deactivate_color
        self.label_width = 0
        self.drop_thick = 1.5
        self.setMinimumHeight(25)
        self.setMinimumWidth(50)
        self.setMouseTracking(True)
        self.lineEdit = PLineEdit(self)
        self.validator = QIntValidator(self.minimum, self.maximum)
        self.init_ui()

    def init_ui(self):

        self.setObjectName("PSpinBox")
        self.setStyleSheet(
            f"#PSpinBox {{background: rgba({self.back_color.red()}, {self.back_color.green()}, {self.back_color.blue()}, 255); "
            f"border-radius: {self.border_radius}; color: rgb({self.text_color.red()}, {self.text_color.green()}, {self.text_color.blue()});}}")
        self.lineEdit.setValidator(self.validator)
        self.lineEdit.setText("0")
        self.lineEdit.textChanged.connect(self.set_value)
        self.lineEdit.focusOut.connect(self.set_last_value)
        self.set_font(QFont("Arial", 14))
        self.setFocusProxy(self.lineEdit)

    def set_single_step(self, step):

        self.singleStep = step

    def set_back_color(self, color):

        self.back_color = color
        self.update()
        self.lineEdit.set_back_color(color)

    def set_text_color(self, color):

        self.text_color = color
        self.lineEdit.set_text_color(color)

    def set_arrow_deactivate_color(self, color):

        self.up_arrow_color = color
        self.down_arrow_color = color

    def set_arrow_color(self, act_color, deact_color):

        self.arrow_activate_color = act_color
        self.arrow_deactivate_color = deact_color
    
    def set_border_radius(self, rad):

        self.border_radius = rad

    def get_maximum(self):

        return self.maximum

    def get_minimum(self):

        return self.minimum

    def set_maximum(self, maxval):

        self.maximum = maxval
        if self.value > maxval:
            self.set_text(maxval)

    def set_minimum(self, minval):

        self.minimum = minval
        if self.value < minval:
            self.set_text(minval)

    def set_range(self, minval, maxval):

        self.set_minimum(minval)
        self.set_maximum(maxval)
        self.validator = QIntValidator(self.minimum, self.maximum)        
        self.lineEdit.setValidator(self.validator)

    def single_step(self):

        return self.singleStep  

    def get_value(self):

        return self.value

    def set_last_value(self):

        self.lineEdit.setText(str(self.value))        

    def set_text(self, val):

        self.lineEdit.setText(str(val))

    def set_value(self, val):

        if val == "" or val == "+" or int(val) < self.minimum or int(val) > self.maximum:
            return
        
        if self.value == int(val):
            return
            
        self.value = int(val)
        self.valueChanged.emit(int(self.value))

    def set_font(self, font):

        self.lineEdit.setFont(font) 

    def set_text_alignment(self, align):

        self.lineEdit.setAlignment(align)        

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Up:
            self.increase()
        if event.key() == Qt.Key_Down:
            self.decrease()

    def wheelEvent(self, event):

        if event.angleDelta().y() > 0:
            self.increase()
        else:
            self.decrease()

    def mouseMoveEvent(self, event):

        tmp_color = self.up_arrow_color
        if self.up_arrow_poly.containsPoint(event.pos(), Qt.OddEvenFill):
            self.setCursor(Qt.PointingHandCursor)
            self.up_arrow_color = self.arrow_activate_color
        else:
            self.setCursor(Qt.ArrowCursor)
            self.up_arrow_color = self.arrow_deactivate_color

        if self.up_arrow_color != tmp_color:
            self.update()
            return

        tmp_color = self.down_arrow_color
        if self.down_arrow_poly.containsPoint(event.pos(), Qt.OddEvenFill):
            self.setCursor(Qt.PointingHandCursor)
            self.down_arrow_color = self.arrow_activate_color
        else:
            self.down_arrow_color = self.arrow_deactivate_color

        if self.down_arrow_color != tmp_color:
            self.update()

    def increase(self):

        if self.value + self.singleStep <= self.maximum:
            self.lineEdit.setText(str(self.value + self.singleStep))
        else:
            self.lineEdit.setText(str(self.maximum))
        self.lineEdit.selectAll()
        self.lineEdit.setFocus()

    def decrease(self):

        if self.value - self.singleStep >= self.minimum:
            self.lineEdit.setText(str(self.value - self.singleStep))
        else:
            self.lineEdit.setText(str(self.minimum))
        self.lineEdit.selectAll()
        self.lineEdit.setFocus()
        
    def mousePressEvent(self, event):

        if self.up_arrow_poly.containsPoint(event.pos(), Qt.OddEvenFill):
            self.increase()
        if self.down_arrow_poly.containsPoint(event.pos(), Qt.OddEvenFill):
            self.decrease()

    def enterEvent(self, event):

        self.hover = True
        self.update()

    def leaveEvent(self, event):

        self.hover = False
        self.update()

    def resizeEvent(self, event):

        self.label_width = self.width() - self.height() * self.rate - self.height() * 2 / 3
        self.lineEdit.setGeometry(self.border_radius, 0, self.label_width - self.border_radius, self.height())
        self.set_border_radius(self.height() / 4)

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)
        if self.hover:
            painter.setBrush(
                QColor(self.back_color.red() + 30, self.back_color.green() + 30, self.back_color.blue() + 30))
            self.lineEdit.set_back_color(QColor(self.back_color.red() + 30, self.back_color.green() + 30, self.back_color.blue() + 30))
        else:
            painter.setBrush(self.back_color)
            self.lineEdit.set_back_color(self.back_color)

        painter.drawRoundedRect(QRect(0, 0, self.width(), self.height()), self.border_radius, self.border_radius)

        pen = QPen(self.down_arrow_color, self.drop_thick, Qt.SolidLine)
        painter.setPen(pen)
        self.down_arrow_poly = QPolygon()
        x1 = QPoint(self.label_width + float(self.height() / 3), float(self.height() * 0.6) )
        x2 = QPoint(self.label_width + float(self.height() / 3) + float(self.height() * self.rate / 2), float(self.height() * 0.75) )
        x3 = QPoint(self.width() - float(self.height() / 3), float(self.height() * 0.6) )
        self.down_arrow_poly << x1 << x2 << x3

        check_path = QPainterPath()
        check_path.moveTo(x1)
        check_path.lineTo(x2)
        check_path.lineTo(x3)
        check_path.lineTo(x1)
        painter.drawPath(check_path)
        if self.down_arrow_color == self.arrow_activate_color:
            painter.fillPath(check_path, QBrush(self.down_arrow_color))
        else:
            if self.hover:
                painter.fillPath(check_path, QColor(self.back_color.red() + 30, self.back_color.green() + 30, self.back_color.blue() + 30))
            else:
                painter.fillPath(check_path, QBrush(self.back_color))

        pen = QPen(self.up_arrow_color, self.drop_thick, Qt.SolidLine)
        painter.setPen(pen)

        x1 = QPoint(self.label_width + float(self.height() / 3), float(self.height() * 0.4) )
        x2 = QPoint(self.label_width + float(self.height() / 3) + float(self.height() * self.rate / 2), float(self.height() * 0.25) )
        x3 = QPoint(self.width() - float(self.height() / 3), float(self.height() * 0.4) )
        self.up_arrow_poly = QPolygon()
        self.up_arrow_poly << x1 << x2 << x3

        check_path = QPainterPath()
        check_path.moveTo(x1)
        check_path.lineTo(x2)
        check_path.lineTo(x3)
        check_path.lineTo(x1)
        painter.drawPath(check_path)        
        if self.up_arrow_color == self.arrow_activate_color:
            painter.fillPath(check_path, QBrush(self.up_arrow_color))
        else:
            if self.hover:
                painter.fillPath(check_path, QColor(self.back_color.red() + 30, self.back_color.green() + 30, self.back_color.blue() + 30))
            else:
                painter.fillPath(check_path, QBrush(self.back_color))

if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication, QVBoxLayout

    app = QApplication()

    w = QWidget()
    w.setObjectName("mainWidget")
    w.setFocusPolicy(Qt.StrongFocus)
    # w.setStyleSheet("#mainWidget {background: rgba(77, 77, 82, 255);}")
    w.setGeometry(0, 0, 400, 600)

    combo = PComboBox(w)
    strs = ['All', 'Advertisement Consent', 'Approval of Matters Specified in Cond.', 'Cert. of Appropriate Alternative Dev.', 'circuit', 'react', 'angular', 'laravel', 'vue', 'Linkedin', 'XING']
    combo.add_items(strs)
    combo.setMaximumHeight(100)
    combo.set_popup_height(150)
    combo.set_text_alignment(Qt.AlignCenter)

    def spinbox_changevalue(text):
        print(text)

    layout = QVBoxLayout(w)
    card1 = PSpinBox(w)
    card1.setMaximumHeight(50)
    card1.set_range(100, 1051)
    card1.set_single_step(3)
    card1.set_text_alignment(Qt.AlignCenter)
    card1.valueChanged.connect(spinbox_changevalue)
    card2 = QFrame(w)
    card3 = QSpinBox(w)
    card3.setValue(10)
    card3.setRange(5, 30)
    card3.setFixedHeight(50)
    card3.setSingleStep(3)

    card4 = QLineEdit(w)
    card4.setFixedHeight(50)
    validator = QIntValidator(100, 500)
    card4.setValidator(validator)

    # print(validator.bottom())
    # print(validator.top())
    pos = 0
    # ret = object
    # ret = validator.validate("501", pos)
    # print(ret)

    # ret = validator.validate("-5", pos)
    # print(ret == QValidator.Invalid)

    # ret = validator.validate("105", pos)
    # print(combo)
    # print(ret == QValidator.Invalid)

    layout.addWidget(combo, 1)
    
    layout.addWidget(card2, 1)
    layout.addWidget(card3, 1)
    layout.addWidget(card4, 1)
    layout.addWidget(card1, 1)
    w.show()
    app.exec_()