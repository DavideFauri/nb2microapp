from PyQt6.QtWidgets import *
from PyQt6.QtCore import QFileInfo, Qt, QSize
from PyQt6.QtGui import *
from pathlib import Path
from nb2microapp.config import Config, Input
from nb2microapp.graphical.alert import alertBox


STYLE_NORMAL = "QLabel{border: 1px dashed #aaa; padding: 0px;}"
# STYLE_NORMAL = "QLabel#dropbox{border: 4px dashed #aaa; padding: 8px;}"
STYLE_ACTIVE = STYLE_NORMAL[:-1] + "background-color: rgba(0,0,255,25%);}"
STYLE_RIGHT = STYLE_NORMAL[:-1] + "background-color: rgba(0,255,0,25%);}"
STYLE_WRONG = STYLE_NORMAL[:-1] + "background-color: rgba(255,0,0,25%);}"


# This label defines a unified style for all droppers
class DropBoxLabel(QLabel):
    def __init__(self, text=""):
        # establishing the objects
        super().__init__()
        self.setObjectName("dropbox")
        self.icon_label = QLabel()
        self.text_label = QLabel()

        self.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Minimum,
        )

        # setting the layout
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        layout.addStretch()
        self.setLayout(layout)

        # setting content and style
        self.initial_text = text
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reset_style()

    def sizeHint(self):
        return QSize(150, 150)

    def reset_style(self):
        self.locked = False
        self.setStyleSheet(STYLE_NORMAL)
        self.text_label.setText(self.initial_text)
        # self.icon_label.clear()
        # self.icon_label.hide()

    def _set_style(
        self,
        styleSheet: str,
        text: str | None = None,
        img: QPixmap | None = None,
        lock_it: bool = False,
    ):
        if not self.locked:
            self.setStyleSheet(styleSheet)
            if text:
                self.text_label.setText(text)
            if img:
                self.icon_label.setScaledPixmap(img, 150, 150)
                # self.icon_label.show()
            self.locked = lock_it

    def set_style_active(self, **kwargs):
        self._set_style(styleSheet=STYLE_ACTIVE, **kwargs)

    def set_style_right(self, **kwargs):
        self._set_style(styleSheet=STYLE_RIGHT, **kwargs)

    def set_style_wrong(self, **kwargs):
        self._set_style(styleSheet=STYLE_WRONG, **kwargs)


# This widget adds file-specific functionalities
class DropBox(QWidget):
    def __init__(self, input: Input):
        super().__init__()
        self.setAcceptDrops(True)
        self.setToolTip(input.tooltip)

        # Parsing filename stuff
        self.input_file = Path(input.name)
        self.input_name = self.input_file.name
        self.input_ext = self.input_file.suffix

        # Styling stuff
        self.setStyleSheet(STYLE_NORMAL)
        self.label = DropBoxLabel(text=f"Trascina qui\n{self.input_name}")
        self.label.setObjectName("dropbox")

        # Layout stuff
        # TODO: work on size policy
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def isValidDroppable(self, event):
        if not event.mimeData().hasUrls():
            return False
        return event.mimeData().urls()[0].isLocalFile()

    def isValidDropExtension(self, filepath):
        return filepath.suffix == self.input_ext

    def dragEnterEvent(self, event: QDragEnterEvent):
        event.accept()
        if not self.isValidDroppable(event):
            self.label.set_style_wrong(text="This is not a file!")
        elif self.input_ext:
            dropped_file = Path(event.mimeData().urls()[0].toLocalFile())
            if self.isValidDropExtension(dropped_file):
                self.label.set_style_right()
            else:
                self.label.set_style_wrong(
                    text=f"This is not a .{self.input_ext} file!"
                )
        else:
            self.label.set_style_active()

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        event.accept()
        if not self.label.locked:
            self.label.reset_style()

    def dropEvent(self, event: QDropEvent):
        event.accept()
        if not self.isValidDroppable(event):
            if not self.label.locked:
                self.label.reset_style()
        elif self.input_ext:
            dropped_file = Path(event.mimeData().urls()[0].toLocalFile())
            if self.isValidDropExtension(dropped_file):
                self.label.set_style_right(text=f"{self.input_name}", lock_it=True)
                self.acceptDrop(dropped_file)
            else:
                self.label.reset_style()
                alertBox(
                    title="Invalid file!",
                    text=f"This file does not seem right: {dropped_file.name}",
                )
        else:
            dropped_file = Path(event.mimeData().urls()[0].toLocalFile())
            self.label.set_style_active(text=f"{self.input_name}", lock_it=True)
            self.acceptDrop(dropped_file)

    def acceptDrop(self, filepath):
        self.input_file = filepath
        icon = QFileIconProvider().icon(QFileInfo(str()))
        pixmap = icon.pixmap(100, 100)
        self.label.setPixmap(pixmap)


class DropBoxesFrame(QFrame):
    def __init__(self, configuration: Config):
        super().__init__()
        self.dropboxes = []
        self.mainLayout = QHBoxLayout()

        # Create each single dropbox
        for f in configuration.input_files:
            self.add_dropbox(f)

        self.setLayout(self.mainLayout)

    def add_dropbox(self, input_file: Input, add_more=False):
        self.dropboxes.append(DropBox(input_file))
        self.mainLayout.addWidget(self.dropboxes[-1])
