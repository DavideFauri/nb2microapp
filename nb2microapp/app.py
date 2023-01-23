import sys
from PyQt6.QtWidgets import QApplication, QFrame, QPushButton, QVBoxLayout, QHBoxLayout
from nb2microapp.config import Config
from nb2microapp.graphical.dropbox import DropBoxesFrame
from nb2microapp.graphical.parameters import ParametersFrame


class App(QApplication):
    def __init__(self, config: Config):
        self.app = QApplication(sys.argv)
        self.window = AppWindow(config)

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())


class AppWindow(QFrame):
    def __init__(self, configuration):
        super().__init__()

        self.setWindowTitle(configuration.app_name)
        mainLayout = QVBoxLayout()

        # first draw the drop boxes
        self.d_frame = DropBoxesFrame(configuration)
        mainLayout.addWidget(self.d_frame, stretch=2)

        # then draw (if available) the flags, input fields, etc.
        self.p_frame = ParametersFrame(configuration)
        mainLayout.addWidget(self.p_frame, stretch=1)

        self.setLayout(mainLayout)
