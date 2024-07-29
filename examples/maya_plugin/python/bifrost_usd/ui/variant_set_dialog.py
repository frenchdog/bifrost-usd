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

from bifrost_usd.author_usd_graph import get_variant_set_names, update_variant_set_names

try:
    from PySide2 import QtWidgets
except ModuleNotFoundError:
    from PySide6 import QtWidgets


class VariantSetCache(object):
    """Store variantSet names so we can re-populate the UI combo box with latest."""

    values: Set[str] = set()
    last_value: str = ""

    def __init__(self, arg):
        super(VariantSetCache, self).__init__()

    @classmethod
    def add(self, tag):
        VariantSetCache.values.add(tag)
        VariantSetCache.last_value = tag

    @classmethod
    def get_last(self):
        if VariantSetCache.values:
            return VariantSetCache.last_value


class VariantSetDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(VariantSetDialog, self).__init__(parent)

        mainLayout = QtWidgets.QVBoxLayout()
        self.vsetGroupBox = QtWidgets.QGroupBox("")
        layout = QtWidgets.QHBoxLayout()

        oldVSetNameLabel = QtWidgets.QLabel("Old VariantSet Name")
        layout.addWidget(oldVSetNameLabel)
        self.oldVSetNameComboBox = self.createOldVSetNameComboBox()
        layout.addWidget(self.oldVSetNameComboBox)

        newVSetNameLabel = QtWidgets.QLabel("New VariantSet Name")
        layout.addWidget(newVSetNameLabel)
        self.newVSetNameComboBox = self.createNewVSetNameComboBox()
        layout.addWidget(self.newVSetNameComboBox)

        self.vsetGroupBox.setLayout(layout)
        mainLayout.addWidget(self.vsetGroupBox)

        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttonBox.accepted.connect(self.verify)
        buttonBox.rejected.connect(self.reject)

        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

        self.newVSetNameComboBox.editTextChanged.connect(self.newVSetNameComboboxUpdate)

        self.setWindowTitle("VariantSet Editor")
        self.resize(600, 120)

    def createOldVSetNameComboBox(self):
        comboBox = QtWidgets.QComboBox()
        comboBox.setEditable(False)
        for name in get_variant_set_names():
            comboBox.addItem(name)

        return comboBox

    def createNewVSetNameComboBox(self):
        comboBox = QtWidgets.QComboBox()
        comboBox.setEditable(True)
        last_hint = VariantSetCache.get_last()
        if last_hint:
            comboBox.addItem(last_hint)
        else:
            comboBox.addItem("")

        for tag in VariantSetCache.values:
            comboBox.addItem(tag)

        return comboBox

    def createButton(self, text, member):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(member)
        return button

    def newVSetNameComboboxUpdate(self, value):
        self.newVSetNameComboBox.setCurrentText(value)

    def verify(self):
        VariantSetCache.add(self.newVSetNameComboBox.currentText())
        update_variant_set_names(
            self.oldVSetNameComboBox.currentText(),
            self.newVSetNameComboBox.currentText(),
        )
        self.accept()
        return


def show():
    dialog = VariantSetDialog(parent=None)
    dialog.exec_()


if __name__ == "__main__":
    show()
