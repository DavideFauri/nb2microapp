from PyQt6.QtWidgets import QMessageBox


def alertBox(*, title, text):
    alert = QMessageBox()
    alert.setWindowTitle(title)
    alert.setText(text)
    _ = alert.exec()
