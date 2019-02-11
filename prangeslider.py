from qtpy.QtCore import Property, QPoint, QRect, Signal, Qt
from qtpy.QtWidgets import QFrame
from qtpy.QtGui import QPainter, QColor

class Handle(QFrame):
	""" Handle widget for range slider """

	handleMoved = Signal()

	def __init__(self, parent = None):
		super().__init__(parent)

		self.value = 0

		self.offset = QPoint()
		self.outer_radius = 0
		self.inner_radius = 0

		self.normal_radius = 0
		self.highlight_radius = 0

		self.borderWidth = 5
		self.xLimit = 0

		self.backColor = QColor(255, 255, 255)
		self.borderColor = QColor(77, 145, 215)

		self.setObjectName("handle")
		self.set_radius(self.outer_radius)

	def set_border_width(self, bw):
		"""
		set border width of handle

		:param bw: border width in integer
		:returns:
		"""

		self.borderWidth = bw

	def set_value(self, value_):
		"""
		set value of handle

		:param value_: value to be set , in integer
		:returns:
		"""

		self.value = value_

	def set_highlight_radius(self, radius_):
		"""
		et radius of handle for the case of highlight

		:param radius_: value to be set, in integer
		:return:
		"""

		self.highlight_radius = radius_

	def set_normal_radius(self, radius_):
		"""
		set radius of handle for the normal case

		:param radius_: value to be set, in integer
		:return:
		"""

		self.normal_radius = radius_
		self.set_radius(self.normal_radius)

	def set_radius(self, radius_):
		"""
		set widget radius

		:param radius_: value to be set, in integer
		:returns:
		"""

		center_x = round(self.x() + float(self.width() / 2))
		center_y = round(self.y() + float(self.height() / 2))

		self.outer_radius = radius_
		self.inner_radius = radius_ - self.borderWidth

		assert(self.outer_radius > self.inner_radius)

		if self.width() == 0 or self.height() == 0:
			self.resize(self.outer_radius * 2, self.outer_radius * 2)
		else:
			self.setGeometry(center_x - self.outer_radius, center_y - self.outer_radius, self.outer_radius * 2, self.outer_radius * 2)

	def mousePressEvent(self, event):
		"""
		mouse press event

		:param event:
		:return:
		"""

		self.offset = event.pos()

	def mouseMoveEvent(self, event):
		"""
		mouse move event

		:param event:
		:return:
		"""

		new_x = self.mapToParent(event.pos()).x() - self.offset.x()

		if self.mapToParent(event.pos()).x() < self.offset.x():
			self.move(0, self.y())
		elif self.mapToParent(event.pos()).x() - self.offset.x() >= self.xLimit:
			self.move(self.xLimit, self.y())
		else:
			self.move(new_x, self.y())

		self.handleMoved.emit()

	def enterEvent(self, event):
		"""
		mouse enter event

		:param event:
		:return:
		"""

		QFrame.enterEvent(self, event)
		self.set_radius(self.highlight_radius)

	def leaveEvent(self, event):
		"""
		mouse leave event

		:param event:
		:return:
		"""

		QFrame.leaveEvent(self, event)
		self.set_radius(self.normal_radius)

	def resizeEvent(self, event):
		"""
		widget resize event

		:param event:
		:return:
		"""

		QFrame.resizeEvent(self, event)

	def paintEvent(self, event):
		"""
		paint event

		:param event:
		:return:
		"""

		#QFrame.paintEvent(self, event)

		painter = QPainter(self)
		painter.setRenderHints(QPainter.Antialiasing)

		painter.setPen(self.borderColor)
		painter.setBrush(self.borderColor)
		painter.drawEllipse(QPoint(self.outer_radius, self.outer_radius), self.outer_radius - 1, self.outer_radius - 1)

		painter.setPen(self.backColor)
		painter.setBrush(self.backColor)
		painter.drawEllipse(QPoint(self.outer_radius, self.outer_radius), self.inner_radius - 1, self.inner_radius - 1)

class PRangeSlider(QFrame):
	""" Customized range slider widget """

	valueChanged = Signal(int, int)

	def __init__(self, parent = None, min = 0, max = 100):
		super().__init__(parent)

		self.range = [0, 100]
		self.interval = 0
		self.isMinLastChanged = True

		self.min = 0
		self.max = 100
		self.horizontal_margin = 0
		self.value_margin = 0

		self.handleNormalSize = 0.75
		self.handleHighlightSize = 1
		self.barSize = 0.2

		self.handle1 = Handle(self)
		self.handle1.set_value(self.min)
		self.handle1.handleMoved.connect(self.update_values)

		self.handle2 = Handle(self)
		self.handle2.set_value(self.max)
		self.handle2.handleMoved.connect(self.update_values)

		self.setObjectName("PRangeSlider")

		self.highlightColor = QColor(77, 145, 215)
		self.disabledColor = QColor(228, 231, 237)
		self.handleColor = QColor(255, 255, 255)

		self.show()

	def set_highlight_color(self, color_):

		self.highlightColor = color_
		self.handle1.borderColor = color_
		self.handle2.borderColor = color_
		self.update()

	def set_disabled_color(self, color_):

		self.disabledColor = color_
		self.update()

	def set_handle_color(self, color_):

		self.handleColor = color_
		self.handle1.backColor = color_
		self.handle2.backColor = color_
		self.update()

	def get_value_from_xpos(self, x_):

		return round(float(x_ - self.value_margin) / float(self.interval))

	def update_values(self):

		value1 = self.get_value_from_xpos(self.handle1.x() + float(self.handle1.width() / 2))
		value2 = self.get_value_from_xpos(self.handle2.x() + float(self.handle2.width() / 2))

		print(value1, value2)

		if value1 > value2:
			if value1 != self.max:
				self.isMinLastChanged = False
			elif value2 != self.min:
				self.isMinLastChanged = True

			if self.min != value2:
				self.min = value2

			if self.max != value1:
				self.max = value1
		else:
			if value2 != self.max:
				self.isMinLastChanged = False
			elif value1 != self.min:
				self.isMinLastChanged = True

			if self.min != value1:
				self.min = value1

			if self.max != value2:
				self.max = value2

		if self.handle1.x() < self.handle2.x():
			self.handle1.set_value(self.min)
			self.handle2.set_value(self.max)
		else:
			self.handle1.set_value(self.max)
			self.handle2.set_value(self.min)

		self.valueChanged.emit(self.min, self.max)
		self.update()

	def set_max_value(self, val_max):

		self.max = val_max

		handle = self.handle1 if self.handle1.value > self.handle2.value else self.handle2

		handle.move(float(self.max * self.interval) + self.horizontal_margin,
						  float((self.height() - self.handle2.height()) / 2));
		handle.set_value(self.max)

		self.valueChanged.emit(self.min, self.max)

	def set_min_value(self, val_min):

		self.min = val_min
		handle = self.handle1 if self.handle1.value < self.handle2.value else self.handle2
		handle.move(self.min * self.interval + self.horizontal_margin,
						  float((self.height() - self.handle1.height()) / 2));
		handle.set_value(self.min)

		self.valueChanged.emit(self.min, self.max)

	def set_range(self, min_ = 0, max_ = 100):

		self.range = [0, 100]

	def mousePressEvent(self, event):

		QFrame.mousePressEvent(self, event)

		value = self.get_value_from_xpos(event.pos().x())

		if value < self.min:
			self.set_min_value(value)
			self.isMinLastChanged = True
		elif value > self.max:
			self.set_max_value(value)
			self.isMinLastChanged = False
		else:
			if self.isMinLastChanged:
				self.set_min_value(value)
				self.isMinLastChanged = True
			else:
				self.set_max_value(value)
				self.isMinLastChanged = False

		self.update()

	def resizeEvent(self, event):

		QFrame.resizeEvent(self, event)

		highlight_radius = self.height() * self.handleHighlightSize / 2
		normal_radius = self.height() * self.handleNormalSize / 2
		x_limit = self.width() - float(self.height() * self.handleHighlightSize)
		border_width = self.height() * float(self.handleHighlightSize - self.handleNormalSize) / 2

		self.handle1.set_highlight_radius(highlight_radius)
		self.handle1.set_normal_radius(normal_radius)
		self.handle1.xLimit = x_limit
		self.handle1.borderWidth = border_width

		self.handle2.set_highlight_radius(highlight_radius)
		self.handle2.set_normal_radius(normal_radius)
		self.handle2.xLimit = x_limit
		self.handle2.borderWidth = border_width

		self.handle1.set_radius(normal_radius)
		self.handle2.set_radius(normal_radius)

		self.horizontal_margin = float(self.height() * float(self.handleHighlightSize - self.handleNormalSize) / 2)
		self.value_margin = float(self.height() * self.handleHighlightSize / 2)

		self.interval = float((self.width() - self.value_margin * 2) / self.range[1])

		self.set_min_value(self.min)
		self.set_max_value(self.max)

	def paintEvent(self, event):

		QFrame.paintEvent(self, event)

		painter = QPainter(self)
		painter.setRenderHints(QPainter.Antialiasing)

		painter.setPen(self.disabledColor)
		painter.setBrush(self.disabledColor)
		x_radius = float(self.height() * self.barSize / 2)
		y_radius = x_radius

		painter.drawRoundedRect(QRect(self.value_margin, (self.height() - self.height() * self.barSize) / 2, self.width() - 2 * self.value_margin, x_radius * 2), x_radius, y_radius)

		painter.setPen(self.highlightColor)
		painter.setBrush(self.highlightColor)
		painter.drawRect(QRect(self.min * self.interval + self.value_margin, (self.height() - self.height() * self.barSize) / 2, self.interval * (self.max - self.min), x_radius * 2))


if __name__ == "__main__":

	from qtpy.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout
	from qtpy.QtGui import QFont
	
	app = QApplication()

	w = QWidget()
	w.setObjectName("mainWidget")
	w.setStyleSheet("#mainWidget {background: white;}")
	w.setGeometry(0, 0, 1200, 120)

	min_label = QLabel(w)
	min_label.setStyleSheet("QLabel {background: rgba(108, 108, 115, 255); border-radius: 9; color: white;}")
	min_label.setFont(QFont("Roboto", 15, QFont.Bold))
	min_label.setAlignment(Qt.AlignCenter)

	max_label = QLabel(w)
	max_label.setStyleSheet("QLabel {background: rgba(108, 108, 115, 255); border-radius: 9; color: white;}")
	max_label.setFont(QFont("Roboto", 15, QFont.Bold))
	max_label.setAlignment(Qt.AlignCenter)

	def print_values(min_, max_):

		min_label.setText(f'{min_}')
		max_label.setText(f'{max_}')

	slider = PRangeSlider(w, 0, 100)
	#slider.set_highlight_color(QColor(145, 75, 215))
	slider.valueChanged.connect(print_values)

	layout = QHBoxLayout(w)

	layout.addWidget(min_label, 1)
	layout.addWidget(slider, 5)
	layout.addWidget(max_label, 1)

	w.show()
	app.exec_()

