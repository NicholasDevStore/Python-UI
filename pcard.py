from qtpy.QtCore import Qt, QRect, QPoint, Signal, QPropertyAnimation
from qtpy.QtWidgets import QFrame, QLabel, QBoxLayout, QHBoxLayout, QWidget, QListWidget, QComboBox
from qtpy.QtGui import QColor, QPainter, QPen, QPainterPath, QPainterPath, QFont, QPalette, QBrush, QPixmap
from elidelabel import ElideLabel
class PCard(QFrame):
    
    def __init__(self, parent = None):

        super().__init__(parent)
        self.setObjectName("PCard")
        self.border_radius = 8
        self.text_color = QColor(255, 255, 255)
        self.lighttext_color = QColor(self.text_color.red() - 30, self.text_color.green() - 30, self.text_color.blue() - 30)
        self.back_color = QColor(108, 108, 115)
        self.title = "30 Barry Rise, Bowdon, Altrincham, Greater Manchester"
        self.homename = "Park_Home"
        self.rooms = "5"
        self.fontSize = 11
        self.font = QFont("Roboto", self.fontSize)
        self.posteddate = "12/10/19"
        self.price = "$20, 000 pcm"
        self.description = "Superb opportunity to purchase this bright and spacious two bedroom flat occupying the two bedroom flat occupying the "
        self.pictures = ['image1.jpg', 'image2.jpg', 'image1.jpg', 'image2.jpg']
        self.init_ui()
        self.set_style()

    def init_ui(self):

        self.pic_label = QLabel(self)
        self.pic_label.setObjectName("PCardPicture")
        self.pic_label.setAutoFillBackground(True)
        self.pic_label.setScaledContents(True)
        self.pic_label.setPixmap(QPixmap(self.pictures[0]))

        self.title_label = ElideLabel(self)
        self.title_label.setObjectName("PCardTitle")
        self.title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.title_label.setText(self.title)
        self.title_label.setWordWrap(True)
        self.set_style_label(self.title_label, 1)

        self.homename_label = QLabel(self)
        self.homename_label.setObjectName("PCardHomeName")
        self.homename_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.homename_label.setText(self.homename)
        self.set_style_label(self.homename_label, 0)

        self.rooms_label = QLabel(self)
        self.rooms_label.setObjectName("PCardRooms")
        self.rooms_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.rooms_label.setText(self.rooms)
        self.set_style_label(self.rooms_label, 0)

        self.posteddate_label = QLabel(self)
        self.posteddate_label.setObjectName("PCardPostedDate")
        self.posteddate_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.posteddate_label.setText("posted " + self.posteddate)
        self.set_style_label(self.posteddate_label, 0)

        self.description_label = ElideLabel(self)
        self.description_label.setObjectName("PCardDescription")
        self.description_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.description_label.setText(self.description)
        self.set_style_label(self.description_label, 0)

        self.price_label = QLabel(self)
        self.price_label.setObjectName("PCardPrice")
        self.price_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.price_label.setText(self.price)
        self.set_style_label(self.price_label, 1)

        self.set_font(self.font)

    def set_font(self, font):

        self.fontSize = font.pointSize()
        self.homename_label.setFont(font)
        self.rooms_label.setFont(font)
        self.posteddate_label.setFont(font)
        self.description_label.setFont(font)
        self.title_label.setFont(QFont(font.family(), self.fontSize + 3, QFont.DemiBold))
        self.price_label.setFont(QFont(font.family(), self.fontSize + 3, QFont.DemiBold))

    def set_style_label(self, label, dark):

        if dark == 0:
            color = self.lighttext_color
        else:
            color = self.text_color

        qssString = f"#{label.objectName()} {{background: rgba({self.back_color.red()}, {self.back_color.green()}, {self.back_color.blue()}, 255);" \
                    f"color: rgb({color.red()}, {color.green()}, {color.blue()}); padding: 2px; }}"

        label.setStyleSheet(qssString)

    def set_border_radius(self, rad):

        self.border_radius = rad
        print(rad)
        self.set_style()

    def set_text_color(self, color):
        self.text_color = color
        self.lighttext_color = QColor(self.text_color.red() - 30, self.text_color.green() - 30,
              self.text_color.blue() - 30)
        self.set_style()

    def set_back_color(self, color):
        self.back_color = color
        self.set_style()        

    def set_style(self):
        self.setStyleSheet(
            f"#PCard {{border-radius: {self.border_radius}; "
            f"background: rgb({self.back_color.red()}, {self.back_color.green()}, {self.back_color.blue()}); "     
            f"color: rgb({self.text_color.red()}, {self.text_color.green()}, {self.text_color.blue()});}}")        

    def resizeEvent(self, event):

        self.setFixedHeight(self.width() * 1.2)
        self.pic_label.setGeometry(0, 0, self.width(), self.height() * 0.61)
        self.title_label.setGeometry(0, self.height() * 0.61, self.width() * 11 / 12, self.height() * 0.12)
        self.homename_label.setGeometry(0, self.height() * 0.73, self.width() / 3, self.height() * 0.07)
        self.rooms_label.setGeometry(self.width() / 3, self.height() * 0.73, self.width() / 6, self.height() * 0.07)
        self.posteddate_label.setGeometry(self.width() / 2, self.height() * 0.73, self.width() / 2, self.height() * 0.07)
        self.description_label.setGeometry(5, self.height() * 0.8, self.width() - 10, self.height() * 0.1)
        self.price_label.setGeometry(self.width() * 0.5, self.height() * 0.9, self.width() * 0.5 - self.border_radius, self.height() * 0.1)
        self.set_border_radius(self.height() / 25)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.back_color)
        painter.drawRoundedRect(QRect(0, 0, self.width(), self.height()), self.border_radius, self.border_radius)

if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication, QVBoxLayout

    app = QApplication()

    w = QWidget()
    w.setObjectName("mainWidget")
    # w.setStyleSheet("#mainWidget {background: rgba(77, 77, 82, 255);}")
    w.setGeometry(0, 0, 720, 403)

    layout = QHBoxLayout(w)
    card1 = PCard(w)
    card2 = PCard(w)

    layout.addWidget(card1, 1)
    layout.addWidget(card2, 1)

    w.show()
    app.exec_()