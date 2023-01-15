from PyQt6.QtWidgets import *
from PyQt6.QtCore import QFileInfo, Qt
from PyQt6.QtGui import *
from pathlib import Path


STYLE_NORMAL = "QLabel#dropbox{border: 4px dashed #aaa; padding: 8px;}"
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

        self.resize(200, 200)
        self.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding,
        )

        # setting the layout
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.icon_label, stretch=0)
        layout.addWidget(self.text_label, stretch=0)
        layout.addStretch()
        self.setLayout(layout)

        # setting content and style
        self.initial_text = text
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reset_style()

    def reset_style(self):
        self.locked = False
        self.setStyleSheet(STYLE_NORMAL)
        self.text_label.setText(self.initial_text)
        self.icon_label.clear()
        self.icon_label.hide()

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
                scaled = img.scaled(
                    width=150,
                    height=150,
                    aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                )
                self.icon_label.setPixmap(scaled)
                self.icon_label.show()
            self.locked = lock_it

    def set_style_active(self, **kwargs):
        self._set_style(styleSheet=STYLE_ACTIVE, **kwargs)

    def set_style_right(self, **kwargs):
        self._set_style(styleSheet=STYLE_RIGHT, **kwargs)

    def set_style_wrong(self, **kwargs):
        self._set_style(styleSheet=STYLE_WRONG, **kwargs)


# This widget adds file-specific functionalities
class DropBox(QWidget):
    def __init__(self, input_file="il tuo file"):
        super().__init__()
        self.setAcceptDrops(True)

        # Parsing filename stuff
        self.input_file_name = Path(input_file).name
        self.input_file_ext = Path(input_file).suffix

        # Styling stuff
        self.setStyleSheet(STYLE_NORMAL)
        self.label = DropBoxLabel(text=f"Trascina qui\n{self.input_file_name}")
        self.label.setObjectName("dropbox")

        # Layout stuff
        # TODO: work on size policy
        self.resize(200, 200)
        self.setSizePolicy(
            QSizePolicy(
                QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
            )
        )
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def isValidDroppable(self, event):
        if not event.mimeData().hasUrls():
            return False
        return event.mimeData().urls()[0].isLocalFile()

    def isValidDropExtension(self, event):
        filepath = Path(event.mimeData().urls()[0].toLocalFile())
        return filepath.suffix == self.input_file_ext

    def alertInvalidDropExtension(self, event):
        filepath = Path(event.mimeData().urls()[0].toLocalFile())
        alert = QMessageBox()
        alert.setWindowTitle("Invalid file!")
        alert.setText("This file does not seem right: " + filepath.name)
        _ = alert.exec()

    def dragEnterEvent(self, event: QDragEnterEvent):
        event.accept()
        if not self.isValidDroppable(event):
            self.label.set_style_wrong(text="This is not a file!")
        elif self.input_file_ext:
            if self.isValidDropExtension(event):
                self.label.set_style_right()
            else:
                self.label.set_style_wrong(
                    text=f"This is not a .{self.input_file_ext} file!"
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
        elif self.input_file_ext:
            if self.isValidDropExtension(event):
                self.label.set_style_right(text=f"{self.input_file_name}", lock_it=True)
                self.acceptDrop(event)
            else:
                self.label.reset_style()
                self.alertInvalidDropExtension(event)
        else:
            self.label.set_style_active(text=f"{self.input_file_name}", lock_it=True)
            self.acceptDrop(event)

    def acceptDrop(self, filepath):
        icon = QFileIconProvider().icon(QFileInfo(str(filepath)))
        pixmap = icon.pixmap(100, 100)
        self.label.setPixmap(pixmap)


class DropBoxes(QWidget):
    def __init__(self, expected_files=[""]):
        assert (
            len(expected_files) >= 1
        ), "The number of expected input files must be greater than 0!"

        self.n_inputs = len(expected_files)
        super().__init__()

        # Set up the user interface
        self.resize(200 * self.n_inputs, 200)
        self.mainLayout = QHBoxLayout()

        for f in expected_files:
            self.mainLayout.addWidget(DropBox(f))

        self.setLayout(self.mainLayout)

    def add_box(self, expected_file=""):
        self.n_inputs += 1
        self.mainLayout.addWidget(DropBox(expected_file))


class LaunchButton(QWidget):
    def __init__(self, action=None):
        super().__init__()

        self.button = QPushButton("Click me")
        self.button.clicked.connect(action)

        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.button)
        layout.addStretch()

        self.setLayout(layout)


class DropWindow(QWidget):
    def __init__(self, expected_files=[""]):
        super().__init__()

        self.resize(200 * len(expected_files), 300)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(DropBoxes(expected_files), stretch=1)
        mainLayout.addWidget(LaunchButton(action=test), stretch=0)

        self.setLayout(mainLayout)


def test():
    print("Lol this is a test")
