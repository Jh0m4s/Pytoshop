from pytoshop.objects.brushes.circle_brush import CircleBrush
from pytoshop.objects.brushes.eraser_brush import EraserBrush

from pytoshop.objects.image_o import Image


class MainController:

    def __init__(self, view):
        self.view = view

        self.control_pressed = False
        self.mouse_pressed = False

    def onControlKeyPressed(self):
        self.control_pressed = True
        self.view.showOpenHandCursor()

    def onControlKeyReleased(self):
        self.control_pressed = False
        self.view.showArrowCursor()

    def onMousePressed(self, event):
        self.mouse_pressed = True

        if self.control_pressed:
            self.startBoard = self.view.drawing_board.pos()
            self.startPoint = event.globalPos()
            self.view.showClosedHandCursor()

    def onMouseMove(self, event):
        if self.mouse_pressed and self.control_pressed:
            end_point = event.globalPos()

            deltaX = end_point.x() - self.startPoint.x()
            deltaY = end_point.y() - self.startPoint.y()

            newX = self.startBoard.x() + deltaX
            newY = self.startBoard.y() + deltaY

            self.view.drawing_board.move(newX, newY)

    def onMouseReleased(self):
        self.mouse_pressed = False

        if self.control_pressed:
            self.view.showOpenHandCursor()

    def onWheel(self, event):
        self.view.drawing_board.controller.onWheel(event.angleDelta().y())
