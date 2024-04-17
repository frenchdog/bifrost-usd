# -
# *****************************************************************************
# Copyright 2024 Autodesk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# *****************************************************************************
# +
from typing import Set

try:
    from PySide2 import QtWidgets
except ModuleNotFoundError:
    from PySide6 import QtWidgets


from bifrost_usd.component_creator.material_hint_attribute import apply_to_selection


class MaterialHint(object):
    """Manage the material hints so we can re-populate the UI combo box with latest hints."""

    values: Set[str] = set()
    last_value: str = ""

    def __init__(self, arg):
        super(MaterialHint, self).__init__()

    @classmethod
    def add(self, tag):
        MaterialHint.values.add(tag)
        MaterialHint.last_value = tag

    @classmethod
    def get_last(self):
        if MaterialHint.values:
            return MaterialHint.last_value


class MaterialHintDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MaterialHintDialog, self).__init__(parent)

        mainLayout = QtWidgets.QVBoxLayout()
        self.matTagGroupBox = QtWidgets.QGroupBox("")
        layout = QtWidgets.QHBoxLayout()

        matTagLabel = QtWidgets.QLabel("Material Hint")
        layout.addWidget(matTagLabel)
        self.hintComboBox = self.createHintComboBox()
        layout.addWidget(self.hintComboBox)

        self.matTagGroupBox.setLayout(layout)
        mainLayout.addWidget(self.matTagGroupBox)

        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttonBox.accepted.connect(self.verify)
        buttonBox.rejected.connect(self.reject)

        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

        self.hintComboBox.editTextChanged.connect(self.hintComboboxUpdate)

        self.setWindowTitle("Set Material Hint")
        self.resize(300, 120)

    def createHintComboBox(self):
        comboBox = QtWidgets.QComboBox()
        comboBox.setEditable(True)
        last_hint = MaterialHint.get_last()
        if last_hint:
            comboBox.addItem(last_hint)
        else:
            comboBox.addItem("")

        for tag in MaterialHint.values:
            comboBox.addItem(tag)

        return comboBox

    def createButton(self, text, member):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(member)
        return button

    def hintComboboxUpdate(self, value):
        self.hintComboBox.setCurrentText(value)

    def verify(self):
        MaterialHint.add(self.hintComboBox.currentText())
        apply_to_selection(self.hintComboBox.currentText())
        self.accept()
        return


def show():
    dialog = MaterialHintDialog(parent=None)
    dialog.exec_()


if __name__ == "__main__":
    show()
