from qtpy.QtCore import Qt, QRect, QPoint, QPointF, Signal, QPropertyAnimation
from qtpy.QtWidgets import QFrame, QLabel, QBoxLayout, QHBoxLayout, QWidget, QListWidget, QComboBox
from qtpy.QtGui import QColor, QPainter, QPen, QPainterPath, QPainterPath, QFont, QPalette, QBrush
from elidelabel import ElideLabel

class PListWidget(QListWidget):
    """ Customized list widget for PComboBox"""

    focusOut = Signal()

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setObjectName("PListWidget")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.verticalScrollBar().setObjectName("PListWidgetScrollBar")
        self.back_color = QColor(139, 139, 148)
        self.text_color = QColor(255, 255, 255)
        self.selected_color = QColor(194, 232, 255)
        self.hover_color = QColor(154, 200, 255)
        self.border_radius = 8
        self.set_style()

    def focusOutEvent(self, event):
        QListWidget.focusOutEvent(self, event)
        self.focusOut.emit()

    def set_back_color(self, color):
        self.back_color = color
        self.set_style()
    
    def set_text_color(self, color):
        self.text_color = color
        self.set_style()

    def set_border_radius(self, rad):
        self.border_radius = rad
        self.set_style()

    def set_hover_color(self, color):
        self.hover_color = color
        self.set_style()

    def set_selected_color(self, color):
        self.selected_color = color
        self.set_style()

    def set_style(self):
        self.setStyleSheet(
            f"#PListWidget {{border-radius: 8px; "
            f"background: rgb({self.back_color.red()}, {self.back_color.green()}, {self.back_color.blue()}); "
            f"color: rgb({self.text_color.red()}, {self.text_color.green()}, {self.text_color.blue()});}} "       
            f"#PListWidget::item:selected:active {{border-radius: 8px; "
            f"background: rgb({self.selected_color.red()}, {self.selected_color.green()}, {self.selected_color.blue()});}} "
            f"#PListWidget::item:hover {{border-radius: 8px; "
            f"background: rgb({self.hover_color.red()}, {self.hover_color.green()}, {self.hover_color.blue()});}}"
        )

        self.verticalScrollBar().setStyleSheet(
            f"#PListWidgetScrollBar:vertical {{background: rgb({self.back_color.red()}, {self.back_color.green()}, {self.back_color.blue()}); "
            f"border-radius: 4px; "
            f"width: 15px; margin: 3px 3px 3px 3px; border: 1px transparent #2A2929;}} "
            f"#PListWidgetScrollBar::handle:vertical {{border-radius: 4px; "
            f"background-color: lightgray; min-height: 5px;}}"
            f"#PListWidgetScrollBar::sub-line:vertical {{margin: 3px 0px 3px 0px; border-image: url(:/qss_icons/rc/up_arrow_disabled.png); "
            f"height: 15px; width: 15px; subcontrol-position: top; subcontrol-origin: margin;}}"
            f"#PListWidgetScrollBar::add-line:vertical {{margin: 3px 0px 3px 0px; border-image: url(:/qss_icons/rc/down_arrow_disabled.png); "
            f"height: 15px; width: 15px; subcontrol-position: bottom; subcontrol-origin: margin;}}"
            f"#PListWidgetScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {{border-image: url(:/qss_icons/rc/up_arrow.png); "
            f"height: 15px; width: 15px; subcontrol-position: top; subcontrol-origin: margin;}}"
            f"#PListWidgetScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {{border-image: url(:/qss_icons/rc/down_arrow.png); "
            f"height: 15px; width: 15px; subcontrol-position: bottom; subcontrol-origin: margin;}}"
            f"#PListWidgetScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{{ background: none; }}"
            f"#PListWidgetScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{{ background: none; }}"
        )            

class PComboBox(QFrame):
    """ Customized combo box """
    currentChanged = Signal(str)

    def __init__(self, parent):
        super().__init__(parent)

        self.rate = 0.25
        self.back_color = QColor(108, 108, 115)
        self.text_color = QColor(255, 255, 255)
        self.hover = False

        self.label_width = 0
        self.drop_thick = 1.5
        self.border_radius = 8
        self.parent = parent
        self.popup_height = 0

        self.setObjectName("PComboBox")
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(25)
        self.setMinimumWidth(50)
        self.init_ui()

    def init_ui(self):
        self.textFrame = QFrame(self)
        self.hTextLayout = QHBoxLayout(self.textFrame)
        self.hTextLayout.setContentsMargins(10, 0, 10, 0)
        self.hTextLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.label = ElideLabel(self.textFrame)
        self.hTextLayout.addWidget(self.label)

        self.popupFrame = QFrame(self.parent)
        self.popupFrame.setObjectName("PComboBoxPopup")

        self.lsWidget = PListWidget(self.parent)

        self.hPopuplayout = QHBoxLayout(self.popupFrame)
        self.hPopuplayout.setContentsMargins(0, 0, 0, 0)
        self.hPopuplayout.addWidget(self.lsWidget)

        self.popupFrame.hide()

        self.lsWidget.currentTextChanged.connect(self.set_current_text)
        self.lsWidget.itemClicked.connect(self.hide_popup)
        self.lsWidget.focusOut.connect(self.hide_popup)

        self.setFocusProxy(self.lsWidget)

        self.set_font(QFont("Arial", 14))

        self.set_border_radius(self.border_radius)

    def set_border_radius(self, radius):

        self.border_radius = radius
        self.lsWidget.set_border_radius(radius)
        self.update_style()

    def set_background_color(self, color):

        self.back_color = color
        self.lsWidget.set_back_color(color)
        self.update_style()

    def set_text_color(self, color):

        self.text_color = color
        self.lsWidget.set_text_color(color)
        self.update_style()

    def update_style(self):

        self.setStyleSheet(
            f"#PComboBox {{border-radius: {self.border_radius}; "
            f"color: rgb({self.text_color.red()}, {self.text_color.green()}, {self.text_color.blue()});}}")

        self.label.setStyleSheet(f"QLabel {{color: rgb({self.text_color.red()}, {self.text_color.green()}, {self.text_color.blue()})}}")

        self.popupFrame.setStyleSheet(
            f"#PComboBoxPopup {{background: rgb({self.back_color.red()}, {self.back_color.green()}, {self.back_color.blue()}); "
            f"border-radius: {self.border_radius}; "
            f"color: rgb({self.text_color.red()}, {self.text_color.green()}, {self.text_color.blue()});}}")

    def set_popup_height(self, height):

        self.popup_height = height

    def add_items(self, texts):

        self.lsWidget.addItems(texts)
        if self.lsWidget.count() > 0:
            self.lsWidget.setCurrentRow(0)

    def clear(self):

        self.lsWidget.clear()
        self.label.setText("")

    def set_current_index(self, row):

        self.lsWidget.setCurrentRow(row)        

    def count(self):

        return self.lsWidget.count()

    def current_index(self):

        return self.lsWidget.currentRow()        

    def set_current_text(self, text):

        self.hide_popup()
        if self.label.text() != text:
            self.label.setText(text)
            self.currentChanged.emit(text)

    def set_font(self, font):

        self.label.setFont(font)        
        self.lsWidget.setFont(font)

    def current_text(self):

        return self.label.text()

    def show_popup(self):
        
        return

    def hide_popup(self):

        self.popupFrame.hide()

    def set_text_alignment(self, align):

        self.hTextLayout.setAlignment(align)

    def find_text(self, text, flags):

        items = self.lsWidget.findItems(text, flags)
        if len(items) == 0:
            return -1
        else:
            return self.lsWidget.row(items[0])

    def enterEvent(self, event):

        self.hover = True
        self.update()

    def leaveEvent(self, event):

        self.hover = False
        self.update()

    def resizeEvent(self, event):

        self.label_width = self.width() - float(self.height() * self.rate) - float(self.height() * 2 / 3)
        self.textFrame.setGeometry(0, 0, self.label_width, self.height())
        self.popupFrame.setGeometry(self.mapToParent(QPoint(0, 0)).x(), self.mapToParent(QPoint(0, 0)).y() + self.height(), self.width(), 150)
        self.set_border_radius(self.height() / 4)

    def mousePressEvent(self, event):

        if not self.popupFrame.isHidden():
            self.hide_popup()
            return

        if self.popup_height == 0:
            self.popupFrame.setFixedHeight((self.lsWidget.fontMetrics().height() + 2) * self.lsWidget.count())
        else:
            self.popupFrame.setFixedHeight(self.popup_height)    

        self.lsWidget.setFocus()
        self.popupFrame.raise_()
        self.popupFrame.show()
    
    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        if self.label_width <= 0:
            return

        painter.setPen(Qt.NoPen)
        if self.hover:
            painter.setBrush(
                QColor(self.back_color.red() + 30, self.back_color.green() + 30, self.back_color.blue() + 30))
        else:
            painter.setBrush(self.back_color)

        painter.drawRoundedRect(QRect(0, 0, self.width(), self.height()), self.border_radius, self.border_radius)

        x1 = QPointF(self.label_width + float(self.height() / 3), float(self.height() * 0.45))
        x2 = QPointF(self.label_width + float(self.height() * (0.66 + self.rate) / 2), float(self.height() * 0.55))
        x3 = QPointF(self.width() - float(self.height() / 3), float(self.height() * 0.45))

        check_path = QPainterPath()
        check_path.moveTo(x1)
        check_path.lineTo(x2)
        check_path.lineTo(x3)

        pen = QPen(self.text_color, self.drop_thick, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawPath(check_path)