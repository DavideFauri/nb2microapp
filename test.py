import sys
from PyQt6.QtWidgets import QApplication
from scaffolding.dropper import DropWindow

TITLE = "Programma di prova"
NAMES_OF_INPUT_FILES = ["File 01", "File 02.csv", "File 03.xlsx"]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DropWindow(expected_files=NAMES_OF_INPUT_FILES)
    window.setWindowTitle(TITLE)
    window.show()
    sys.exit(app.exec())
