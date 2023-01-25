import sys
from PyQt6.QtWidgets import QApplication, QFrame, QPushButton, QVBoxLayout, QHBoxLayout
from nb2microapp.config import Config
from nb2microapp.graphical.dropboxes import DropBoxesFrame
from nb2microapp.graphical.parameters import ParametersFrame


class App(QApplication):
    def __init__(self, config: Config):
        self.app = QApplication(sys.argv)
        self.window = AppWindow(config)

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())


class AppWindow(QFrame):
    def __init__(self, configuration: Config):
        super().__init__()
        self.configuration = configuration

        self.setWindowTitle(self.configuration.app_name)
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)

        # first draw the drop boxes
        self.d_frame = DropBoxesFrame(self.configuration)
        mainLayout.addWidget(self.d_frame, stretch=2)

        # then draw (if available) the flags, input fields, etc.
        self.p_frame = ParametersFrame(self.configuration)
        mainLayout.addWidget(self.p_frame, stretch=1)

        # then draw the launch button
        self.b_frame = ButtonFrame(action=self.callback)
        mainLayout.addWidget(self.b_frame, stretch=0)

        self.setLayout(mainLayout)

    def callback(self):
        print(self.configuration.to_dict())


class ButtonFrame(QFrame):
    def __init__(self, action=None):
        super().__init__()

        self.button = QPushButton("Click me")
        self.action = action
        self.button.clicked.connect(self.launch)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.button)
        layout.addStretch()

        self.setLayout(layout)

    def launch(self):
        self.setFocus()
        self.action()
        self.parent().close()
