import sys
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction

class ResizableWindow(QMainWindow):
    windows = []
    RESIZE_MARGIN = 10

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Redact")
        self.setStyleSheet("background-color: black;")
        self.setGeometry(100, 100, 400, 400)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.dragging = False
        self.resizing = False
        self.resize_direction = None

        # Menu bar setup
        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        window_menu = menubar.addMenu("Window")

        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_window)
        window_menu.addAction(new_action)

        self.oldPos = self.pos()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        if event.button() == Qt.RightButton:
            self.close()
        elif event.button() == Qt.LeftButton:
            self.resizing, self.resize_direction = self.detect_resize_region(event.pos())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.resizing:
            self.perform_resize(event.globalPos())
        elif event.buttons() == Qt.LeftButton and not self.resizing:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.resizing = False

    def detect_resize_region(self, pos):
        rect = self.rect()
        resizing = False
        direction = None

        # Detect corners and sides
        if pos.y() < self.RESIZE_MARGIN:
            if pos.x() < self.RESIZE_MARGIN:
                direction = Qt.TopLeftCorner
            elif pos.x() > rect.width() - self.RESIZE_MARGIN:
                direction = Qt.TopRightCorner
            else:
                direction = Qt.TopEdge
        elif pos.y() > rect.height() - self.RESIZE_MARGIN:
            if pos.x() < self.RESIZE_MARGIN:
                direction = Qt.BottomLeftCorner
            elif pos.x() > rect.width() - self.RESIZE_MARGIN:
                direction = Qt.BottomRightCorner
            else:
                direction = Qt.BottomEdge
        elif pos.x() < self.RESIZE_MARGIN:
            direction = Qt.LeftEdge
        elif pos.x() > rect.width() - self.RESIZE_MARGIN:
            direction = Qt.RightEdge

        resizing = direction is not None
        return resizing, direction

    def perform_resize(self, globalPos):
        rect = self.geometry()
        if self.resize_direction in [Qt.TopLeftCorner, Qt.LeftEdge, Qt.BottomLeftCorner]:
            rect.setLeft(globalPos.x())
        if self.resize_direction in [Qt.TopLeftCorner, Qt.TopEdge, Qt.TopRightCorner]:
            rect.setTop(globalPos.y())
        if self.resize_direction in [Qt.BottomLeftCorner, Qt.BottomEdge, Qt.BottomRightCorner]:
            rect.setBottom(globalPos.y())
        if self.resize_direction in [Qt.TopRightCorner, Qt.RightEdge, Qt.BottomRightCorner]:
            rect.setRight(globalPos.x())

        self.setGeometry(rect)

    def new_window(self):
        new_win = ResizableWindow()
        new_win.show()
        ResizableWindow.windows.append(new_win)

def main():
    app = QApplication(sys.argv)
    window = ResizableWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
