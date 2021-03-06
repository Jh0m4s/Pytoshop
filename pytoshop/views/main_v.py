from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDesktopWidget, QWidget, QGridLayout, QFileDialog

from pytoshop.controllers.main_c import MainController
from pytoshop.objects.tools.brushes.eraser_o import Eraser
from pytoshop.objects.tools.brushes.paint_o import Paint
from pytoshop.objects.tools.brushes.pencil_o import Pencil
from pytoshop.objects.tools.hand_o import Hand
from pytoshop.objects.tools.move_o import Move
from pytoshop.objects.tools.text_o import Text
from pytoshop.objects.tools.zoom_o import Zoom
from pytoshop.views.main.drawing_board_v import DrawingBoardView
from pytoshop.views.main.layers_v import LayersView
from pytoshop.views.main.menu_bar_v import MenuBarView
from pytoshop.views.main.tool_bar_v import ToolBarView
from pytoshop.views.main.top_bar_v import TopBarView


class MainView(QWidget):

    def __init__(self, app, image_width=500, image_height=500, image_color=(255, 255, 255, 255)):
        super().__init__()
        self.app = app
        self.controller = MainController(self)

        self.initGeometry(800, 520)

        self.tools = {"paint": Paint(),
                      "pencil": Pencil(),
                      "eraser": Eraser(),
                      "text": Text(),
                      "zoom": Zoom(),
                      "select": Hand(),
                      "move": Move()
                      }
        self.topBar = TopBarView(self.tools)
        self.toolbar = ToolBarView(self, 'pytoshop/views/images/toolBarImages/', self.tools)
        self.drawing_board = DrawingBoardView(self, image_width, image_height, image_color)
        self.menuBar = MenuBarView(self)
        self.layers = LayersView(self, self.drawing_board.controller.image)

        layout = QGridLayout()
        layout.addWidget(self.topBar, 1, 1, 1, 10)
        layout.addWidget(self.toolbar, 2, 1, 8, 1)  # addWidget(row, col, rowspan == height, colspan == width)
        invisible = QWidget()
        invisible.hide()
        layout.addWidget(invisible, 2, 2, 8, 8)
        layout.addWidget(self.layers, 2, 10, 8, 1)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(p)
        self.setLayout(layout)

    def initGeometry(self, width, height):
        # Set size
        self.setGeometry(0, 0, width, height)

        # Center window
        frame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())

    # EVENTS #

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.controller.onControlKeyPressed()
        elif event.key() == Qt.Key_Alt:
            self.controller.onAltKeyPressed()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.controller.onControlKeyReleased()
        elif event.key() == Qt.Key_Alt:
            self.controller.onAltKeyReleased()

    def mousePressEvent(self, event):
        self.controller.onMousePressed(event)

    def mouseReleaseEvent(self, event):
        self.controller.onMouseReleased()

    def mouseMoveEvent(self, event):
        self.controller.onMouseMove(event)

    def wheelEvent(self, event):
        self.controller.onWheel(event)

    # FUNCTIONS #

    def hideCursor(self):
        QApplication.setOverrideCursor(Qt.BlankCursor)

    def showOpenHandCursor(self):
        QApplication.setOverrideCursor(Qt.OpenHandCursor)

    def showClosedHandCursor(self):
        QApplication.setOverrideCursor(Qt.ClosedHandCursor)

    def showArrowCursor(self):
        QApplication.setOverrideCursor(Qt.ArrowCursor)

    # POPUPS #
    def loadImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "png (*.png)", options=options)

        if filePath:
            self.drawing_board.controller.image.load(self, filePath)
            self.drawing_board.refresh()
            self.layers.refresh()

    def saveImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "png (*.png)", options=options)

        if filePath:
            self.drawing_board.controller.image.save(filePath)