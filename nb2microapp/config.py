import json


class Param:
    def __init__(self, json_data):
        self.name = json_data["name"]
        self.tooltip = json_data["tooltip"] if "tooltip" in json_data else None


class Input(Param):
    def __init__(self, json_data):
        super().__init__(json_data)


class Flag(Param):
    def __init__(self, json_data):
        super().__init__(json_data)


class TextField(Param):
    def __init__(self, json_data):
        super().__init__(json_data)


class Choices(Param):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.options = json_data["options"]


class Config:
    def __init__(self, json_path):

        with open(json_path, "r") as config_file:
            config = json.load(config_file)

            # parse the app name
            assert (
                "app_name" in config
            ), "The configuration file does not specify an app name!"
            self.app_name = config["app_name"]

            # parse the notebook path
            assert (
                "notebook" in config
            ), "The configuration file does not specify a notebook filename!"
            self.notebook = config["notebook"]

            # parse the input files
            assert (
                "inputs" in config and len(config["inputs"]) > 0
            ), "The configuration file does not specify the input files!"
            self.input_files = []
            for input_file in config["inputs"].values():
                self.input_files.append(Input(input_file))

            # parse the configuration flags
            self.flags = []
            for flag in config["flags"].values():
                self.flags.append(Flag(flag))

            # parse the configuration text fields
            self.text_fields = []
            for text_field in config["text_fields"].values():
                self.text_fields.append(TextField(text_field))

            # parse the configuration choice menus
            self.choices = []
            for choice in config["choices"].values():
                self.choices.append(Choices(choice))
