import os
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout


class ToolBarView(QWidget):

    def __init__(self, parent, icon_directory, tools):
        super().__init__()

        self.parent = parent
        self.tools = tools
        self.setFixedWidth(40)
        self.buttons = {}

        layout = QVBoxLayout()

        for filename in os.listdir(icon_directory):
            button = QPushButton(QIcon(icon_directory + filename), '', parent)
            button.setCheckable(True)
            button.clicked.connect(partial(self.pressButton, filename.split(".")[0]))
            self.buttons[filename.split(".")[0]] = button
            layout.addWidget(button)

        self.buttons['brush'].setChecked(True)
        self.currentButton = self.buttons['brush']

        layout.addStretch()
        self.setLayout(layout)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.darkGray)
        self.setPalette(p)

    # 1. set the current tool to the currently pressed tool
    # 2. unchecks the previous tool
    def pressButton(self, name):
        self.currentButton.setChecked(False)
        self.parent.drawing_board.controller.tool = self.tools[name]
        self.currentButton = self.buttons[name]
        self.currentButton.setChecked(True)
