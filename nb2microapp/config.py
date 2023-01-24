import json
from pathlib import Path
from string import ascii_letters, digits
from itertools import chain

PARAM_TYPES = ["files", "flags", "texts", "choices"]


class Param:
    def __init__(self, identifier: str, json_data: dict, value=None):
        self.identifier = identifier
        assert "name" in json_data, f"There is no descriptive name for {identifier}!"
        self.name = json_data["name"]
        self.tooltip = json_data["tooltip"] if "tooltip" in json_data else None
        self.value = value

    def __str__(self):
        return f"{self.identifier}: {self.value}"


class File(Param):
    def __init__(self, identifier, json_data):
        super().__init__(identifier, json_data, value=None)


class Flag(Param):
    def __init__(self, identifier, json_data):
        super().__init__(identifier, json_data, value=False)


class Text(Param):
    def __init__(self, identifier, json_data):
        super().__init__(identifier, json_data, value="")


class Choice(Param):
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
            "files" in config and len(config["files"]) > 0
        ), "The configuration file does not specify the input files!"

        allowed_characters = set(ascii_letters + digits + "_")
        for group in PARAM_TYPES:
            if group in config:
                for identifier_string in config[group].keys():
                    assert (
                        set(identifier_string) <= allowed_characters
                    ), f"The identifier '{item_name}' contains spaces or other unallowed characters!"

        all_IDs = list(
            chain.from_iterable([ID for ID in config[p].keys()] for p in PARAM_TYPES)
        )
        assert len(all_IDs) == len(
            set(all_IDs)
        ), "Two or more identifiers have the same name!"

    def __init__(self, config_json: str | Path):

        config = self.load(config_json)
        self.validate(config)

        self.app_name = config["app_name"]
        self.notebook = config["notebook"]
        self.files = [File(ID, i) for ID, i in config["files"].items()]
        if "flags" in config:
            self.flags = [Flag(ID, f) for ID, f in config["flags"].items()]
        if "texts" in config:
            self.texts = [Text(ID, t) for ID, t in config["texts"].items()]
        if "choices" in config:
            self.choices = [Choice(ID, c) for ID, c in config["choices"].items()]

    def to_dict(self) -> dict:
        d = {}
        d["app_name"] = self.app_name
        d["notebook"] = self.notebook
        d["files"] = dict([(i.identifier, i.value) for i in self.files])
        if self.flags:
            d["flags"] = dict([(f.identifier, f.value) for f in self.flags])
        if self.texts:
            d["texts"] = dict([(t.identifier, t.value) for t in self.texts])
        if self.choices:
            d["choices"] = dict([(c.identifier, c.value) for c in self.choices])
        return d
