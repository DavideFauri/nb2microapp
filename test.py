import sys
from PyQt6.QtWidgets import QApplication
from nb2microapp.config import Config
import json


CONFIGURATION_FILE = "config.json"


if __name__ == "__main__":

    config = Config(CONFIGURATION_FILE)
    print(config)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = DropWindow(expected_files=NAMES_OF_INPUT_FILES)
#     window.setWindowTitle(TITLE)
#     window.show()
#     sys.exit(app.exec())
