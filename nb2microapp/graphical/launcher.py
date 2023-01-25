from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox,
)
from PyQt6.QtCore import QUrl


class ExportLink(QLabel):
    def __init__(self, link_text: str):
        self.link_text = link_text
        super().__init__(f"<small>{link_text}</>")

    def set_link(self, filepath):
        self.link = bytearray(QUrl.fromLocalFile(filepath).toEncoded()).decode()
        self.setText(f"<small><a href='{self.link}'>{self.link_text}</></>")
        self.setOpenExternalLinks(True)


class LaunchButton(QPushButton):
    def __init__(self):
        super().__init__("Launch")


class SaveHTMLFlag(QCheckBox):
    def __init__(self):
        super().__init__("Save HTML")


class LauncherFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.nb_link = ExportLink("View notebook")
        self.nb_link.setToolTip("View the .ipynb notebook file used to build this app")
        self.conf_link = ExportLink("View configuration")
        self.conf_link.setToolTip(
            "View the JSON configuration file used to build this app"
        )
        self.button = LaunchButton()
        self.saveHTML = SaveHTMLFlag()

        link_frame = QFrame()
        link_layout = QVBoxLayout()
        link_layout.setSpacing(0)
        link_layout.addWidget(self.nb_link)
        link_layout.addWidget(self.conf_link)
        link_frame.setLayout(link_layout)

        layout = QHBoxLayout()
        layout.addWidget(link_frame)
        # layout.addStretch()
        layout.addWidget(self.button)
        layout.addWidget(self.saveHTML)
        # layout.addStretch()
        self.setLayout(layout)
