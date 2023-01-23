import json
from pathlib import Path
from string import ascii_letters, digits


class Param:
    def __init__(self, identifier: str, json_data: dict, value=None):
        self.identifier = identifier
        assert "name" in json_data, f"There is no descriptive name for {identifier}!"
        self.name = json_data["name"]
        self.tooltip = json_data["tooltip"] if "tooltip" in json_data else None
        self.value = value


class Input(Param):
    def __init__(self, identifier, json_data):
        super().__init__(identifier, json_data, value=None)


class Flag(Param):
    def __init__(self, identifier, json_data):
        super().__init__(identifier, json_data, value=False)


class TextField(Param):
    def __init__(self, identifier, json_data):
        super().__init__(identifier, json_data, value="")


class Choices(Param):
    def __init__(self, identifier, json_data):
        assert (
            "options" in json_data and len(json_data["options"]) > 0
        ), f"There are no options specified for {identifier}!"
        super().__init__(identifier, json_data, value=json_data["options"][0])
        self.options = json_data["options"]


class Config:
    @classmethod
    def load(cls, config_json: str | Path) -> dict:

        try:
            if Path(config_json).is_file():
                # option 1, we are provided a path to a json file
                with open(config_json, "r") as config_file:
                    config = json.load(config_file)
            else:
                # option 2, we are provided a json string
                config = json.load(config_json)
        except e:
            alertBox(
                title="Invalid configuration!",
                text="The provided configuration might not be a JSON.",
            )
            raise e

        return config

    @classmethod
    def validate(cls, config: dict) -> None:
        assert (
            "app_name" in config
        ), "The configuration file does not specify an app name!"
        assert (
            "notebook" in config
        ), "The configuration file does not specify a notebook filename!"
        assert (
            "inputs" in config and len(config["inputs"]) > 0
        ), "The configuration file does not specify the input files!"

        allowed_characters = set(ascii_letters + digits + "_")
        for group in ["inputs", "flags", "text_fields", "choices"]:
            if group in config:
                for identifier_string in config[group].keys():
                    assert (
                        set(identifier_string) <= allowed_characters
                    ), f"The identifier '{item_name}' contains spaces or other unallowed characters"

    def __init__(self, config_json: str | Path):

        config = self.load(config_json)
        self.validate(config)

        self.app_name = config["app_name"]
        self.notebook = config["notebook"]
        self.input_files = [Input(ID, i) for ID, i in config["inputs"].items()]
        self.flags = [Flag(ID, f) for ID, f in config["flags"].items()]
        self.text_fields = [TextField(ID, t) for ID, t in config["text_fields"].items()]
        self.choices = [Choices(ID, c) for ID, c in config["choices"].items()]
