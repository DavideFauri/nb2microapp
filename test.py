import sys
from nb2microapp.config import Config
from nb2microapp.app import App
import json


CONFIGURATION_FILE = "config.json"


if __name__ == "__main__":

    config = Config(CONFIGURATION_FILE)
    app = App(config)
    app.run()
