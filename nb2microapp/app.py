import sys
from PyQt6.QtWidgets import QApplication, QFrame, QPushButton, QVBoxLayout, QHBoxLayout
from nb2microapp.config import Config
from nb2microapp.graphical.dropboxes import DropBoxesFrame
from nb2microapp.graphical.parameters import ParametersFrame
from nb2microapp.graphical.launcher import LauncherFrame


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

        # then draw the launch button and other stuff
        self.l_frame = LauncherFrame()
        mainLayout.addWidget(self.l_frame, stretch=0)

        # then connect all the things to the launcher frame
        self.l_frame.nb_link.set_link(configuration.notebook)
        self.l_frame.conf_link.set_link("config.json")
        self.l_frame.button.clicked.connect(self.launch)

        self.setLayout(mainLayout)

    def launch(self):
        self.l_frame.button.setFocus()
        if self.l_frame.saveHTML.isChecked():
            print("saving as HTML")
        print(self.configuration.to_dict())
        self.close()
