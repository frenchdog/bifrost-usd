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

from bifrost_usd.constants import kPrimNodeList
from bifrost_usd.author_usd_graph import (
    get_prim_paths_from_node_types,
    update_prim_path,
)

try:
    from PySide2 import QtWidgets
except ModuleNotFoundError:
    from PySide6 import QtWidgets


class PrimPathCache(object):
    """Store prim paths so we can re-populate the UI combo box with latest."""

    values: Set[str] = set()
    last_value: str = ""

    def __init__(self, arg):
        super(PrimPathCache, self).__init__()

    @classmethod
    def add(self, tag):
        PrimPathCache.values.add(tag)
        PrimPathCache.last_value = tag

    @classmethod
    def get_last(self):
        if PrimPathCache.values:
            return PrimPathCache.last_value


class PrimPathDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PrimPathDialog, self).__init__(parent)

        mainLayout = QtWidgets.QVBoxLayout()
        self.groupBox = QtWidgets.QGroupBox("")
        layout = QtWidgets.QHBoxLayout()

        oldPrimPathLabel = QtWidgets.QLabel("Old Prim Path")
        layout.addWidget(oldPrimPathLabel)
        self.oldPrimPathComboBox = self.createOldPrimPathComboBox()
        layout.addWidget(self.oldPrimPathComboBox)

        newPrimPathLabel = QtWidgets.QLabel("New Prim Path")
        layout.addWidget(newPrimPathLabel)
        self.newPrimPathComboBox = self.createNewPrimPathComboBox()
        layout.addWidget(self.newPrimPathComboBox)

        self.groupBox.setLayout(layout)
        mainLayout.addWidget(self.groupBox)

        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttonBox.accepted.connect(self.verify)
        buttonBox.rejected.connect(self.reject)

        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

        self.newPrimPathComboBox.editTextChanged.connect(self.primPathComboboxUpdate)

        self.setWindowTitle("Prim Path Editor")
        self.resize(600, 120)

    def createOldPrimPathComboBox(self):
        comboBox = QtWidgets.QComboBox()
        comboBox.setEditable(False)
        for name in get_prim_paths_from_node_types(kPrimNodeList):
            comboBox.addItem(name)

        return comboBox

    def createNewPrimPathComboBox(self):
        comboBox = QtWidgets.QComboBox()
        comboBox.setEditable(True)
        last_hint = PrimPathCache.get_last()
        if last_hint:
            comboBox.addItem(last_hint)
        else:
            comboBox.addItem("")

        for tag in PrimPathCache.values:
            comboBox.addItem(tag)

        return comboBox

    def createButton(self, text, member):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(member)
        return button

    def primPathComboboxUpdate(self, value):
        self.newPrimPathComboBox.setCurrentText(value)

    def verify(self):
        PrimPathCache.add(self.newPrimPathComboBox.currentText())
        update_prim_path(
            self.oldPrimPathComboBox.currentText(),
            self.newPrimPathComboBox.currentText(),
        )
        self.accept()
        return


def show():
    dialog = PrimPathDialog(parent=None)
    dialog.exec_()


if __name__ == "__main__":
    show()
