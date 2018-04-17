import sys
sys.path.append('..')

from pytoshop.controllers.main_c import MainController,DrawingBoardController
from pytoshop.objects.brush_o import Brush

from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QLabel
from PyQt5.QtGui import QImage,QPixmap,QPainter
from PyQt5.QtCore import Qt

class DrawingBoard(QLabel):

    def __init__(self, parent, width, height, image_name=None):
        super().__init__(parent)
        self.controller = DrawingBoardController(parent.controller, self)
        self.controller.createImage(500, 500)
        self.brush = Brush()
        
    def displayImage(self, image):
        image = QImage(image.value, image.width, image.height, image.bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap(image)
        self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        self.controller.onMousePressed(event)

    def mouseMoveEvent(self, event):
        self.controller.onMouseMove(event)

class MainView(QWidget):

    def __init__(self):
        super().__init__()

        self.controller = MainController(self)
        self.drawing_board = DrawingBoard(self, 500, 500)

        self.setGeometry(0, 0, 600, 600)

    # EVENTS #

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.controller.onControlPressed()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.controller.onControlReleased()

    def mousePressEvent(self, event):
        self.controller.onMousePressed(event.globalPos())

    def mouseReleaseEvent(self, event):
        self.controller.onMouseReleased()

    def mouseMoveEvent(self, event):
        self.controller.onMouseMove(event.globalPos())

    # FUNCTIONS #

    def showOpenHandCursor(self):
        QApplication.setOverrideCursor(Qt.OpenHandCursor)

    def showClosedHandCursor(self):
        QApplication.setOverrideCursor(Qt.ClosedHandCursor)

    def showArrowCursor(self):
        QApplication.setOverrideCursor(Qt.ArrowCursor)