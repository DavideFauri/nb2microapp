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
        super().__init__()
        self.param = flag
        self.setText(flag.name)
        self.setToolTip(flag.tooltip)
        self.stateChanged.connect(self.set_flag)

    def set_flag(self):
        self.param.value = self.isChecked()
        print(self.param.value)


class TextBox(QLineEdit):
    def __init__(self, text: Text):
        super().__init__()
        self.param = text
        self.setPlaceholderText(text.name)
        self.setToolTip(text.tooltip)
        self.editingFinished.connect(self.set_text)

    def set_text(self):
        self.param.value = self.text()
        print(self.param.value)


class ChoiceBox(QComboBox):
    def __init__(self, choice: Choice):
        super().__init__()
        self.param = choice
        self.setPlaceholderText(choice.name)
        self.insertItems(0, choice.options)
        self.setToolTip(choice.tooltip)
        self.activated.connect(self.set_choice)

    def set_choice(self):
        self.param.value = self.currentText()
        print(self.param.value)


class ParametersFrame(QFrame):
    def __init__(self, configuration: Config):
        super().__init__()
        self.params = []
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)

        # Create the parameter frames, one for each param type
        self.make_param_frame(configuration.flags)
        self.make_param_frame(configuration.texts)
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
            elif typ is Text:
                layout.addWidget(TextBox(param))
            elif typ is Choice:
                layout.addWidget(ChoiceBox(param))
            else:
                print(type(param))
        frame.setLayout(layout)

        self.mainLayout.addWidget(frame)
