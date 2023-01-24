from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QLineEdit,
    QComboBox,
)
from nb2microapp.config import *


class FlagBox(QCheckBox):
    def __init__(self, flag: Flag):
        super().__init__(flag.name)
        self.flag = flag
        self.stateChanged.connect(self.set_flag)
        self.setToolTip(self.flag.tooltip)

    def set_flag(self):
        self.flag.value = self.isChecked()
        print(self.flag.value)


class TextFieldBox(QLineEdit):
    def __init__(self, text_field: TextField):
        super().__init__()
        self.setPlaceholderText(text_field.name)
        self.text_field = text_field
        self.editingFinished.connect(self.set_text)
        self.setToolTip(self.text_field.tooltip)

    def set_text(self):
        self.text_field.value = self.text()
        print(self.text_field.value)


class ChoicesBox(QComboBox):
    def __init__(self, choices: Choices):
        super().__init__()
        self.setPlaceholderText(choices.name)
        self.insertItems(0, choices.options)
        self.choices = choices
        self.activated.connect(self.set_choice)
        self.setToolTip(self.choices.tooltip)

    def set_choice(self):
        self.choices.value = self.currentText()
        print(self.choices.value)


class ParametersFrame(QFrame):
    def __init__(self, configuration: Config):
        super().__init__()
        self.params = []
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)

        # Create the parameter frames, one for each param type
        self.make_param_frame(configuration.flags)
        self.make_param_frame(configuration.text_fields)
        self.make_param_frame(configuration.choices)

        self.setLayout(self.mainLayout)

    def make_param_frame(self, parameters: [Param]) -> QFrame:
        if len(parameters) == 0:
            return

        frame = QFrame()
        layout = QHBoxLayout()
        for param in parameters:
            typ = type(param)
            if typ is Flag:
                layout.addWidget(FlagBox(param))
            elif typ is TextField:
                layout.addWidget(TextFieldBox(param))
            elif typ is Choices:
                layout.addWidget(ChoicesBox(param))
            else:
                print(type(param))
        frame.setLayout(layout)

        self.mainLayout.addWidget(frame)
