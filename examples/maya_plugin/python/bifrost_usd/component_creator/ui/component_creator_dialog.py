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
import os

try:
    from PySide2 import QtWidgets
except ModuleNotFoundError:
    from PySide6 import QtWidgets


from maya import cmds
from bifrost_usd.component_creator import constants
from bifrost_usd.component_creator.component import component_creator
from bifrost_usd.component_creator.component import load_plugin_if_needed
from bifrost_usd.component_creator.component import hasComponentCreatorGraph


class ComponentCreatorDialog(QtWidgets.QDialog):
    currentDir = os.getenv(
        "BIFROST_USD_LAB_COMPONENT_ROOT_DIR", cmds.workspace(q=True, dir=True)
    )

    def __init__(self, parent=None):
        super(ComponentCreatorDialog, self).__init__(parent)

        directoryLabel = QtWidgets.QLabel("Component Directory")
        self.directoryComboBox = self.createDirectoryComboBox(
            ComponentCreatorDialog.currentDir
        )
        self.directoryComboBox.currentIndexChanged.connect(self.update_versions)
        self.browseButton = self.createButton("&Browse...", self.browse)

        self.versionLabel = QtWidgets.QLabel("Asset Version")
        self.versionComboBox = self.createVersionComboBox()

        mainLayout = QtWidgets.QGridLayout()

        row = 0

        mainLayout.addWidget(directoryLabel, row, 0)
        mainLayout.addWidget(self.directoryComboBox, row, 1)
        mainLayout.addWidget(self.browseButton, row, 2)
        row += 1

        mainLayout.addWidget(self.versionLabel, row, 0)
        mainLayout.addWidget(self.versionComboBox, row, 1, 1, 2)
        row += 1

        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )

        buttonBox.accepted.connect(self.verify)
        buttonBox.rejected.connect(self.reject)

        mainLayout.addWidget(buttonBox, row, 1, 1, 2)

        self.setLayout(mainLayout)

        self.setWindowTitle("Component Creator")
        self.resize(600, 100)

        self.update_versions()

    def createDirectoryComboBox(self, text=""):
        comboBox = QtWidgets.QComboBox()
        comboBox.setEditable(False)
        if text:
            comboBox.addItem(text)
        return comboBox

    def createVersionComboBox(self):
        comboBox = QtWidgets.QComboBox()
        comboBox.setEditable(False)
        return comboBox

    def createButton(self, text, member):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(member)
        return button

    def browse(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Select Component Directory",
            ComponentCreatorDialog.currentDir,
            QtWidgets.QFileDialog.ShowDirsOnly
            | QtWidgets.QFileDialog.ReadOnly
            | QtWidgets.QFileDialog.DontUseNativeDialog
            | QtWidgets.QFileDialog.HideNameFilterDetails,
        )

        if directory:
            if self.directoryComboBox.findText(directory) == -1:
                self.directoryComboBox.addItem(directory)

            self.directoryComboBox.setCurrentIndex(
                self.directoryComboBox.findText(directory)
            )

            ComponentCreatorDialog.currentDir = self.directoryComboBox.currentText()
            self.update_versions()

    def update_versions(self):
        self.versionComboBox.clear()
        if os.path.isdir(ComponentCreatorDialog.currentDir):
            if os.path.isfile(
                os.path.join(ComponentCreatorDialog.currentDir, ".versions")
            ):
                versions = []

                for name in os.listdir(ComponentCreatorDialog.currentDir):
                    if os.path.isfile(
                        os.path.join(ComponentCreatorDialog.currentDir, name)
                    ):
                        continue
                    versions.append(name)

                for name in sorted(versions, reverse=True):
                    self.versionComboBox.addItem(name)

        if self.versionComboBox.count() == 0:
            self.versionLabel.hide()
            self.versionComboBox.hide()
        else:
            self.versionLabel.show()
            self.versionComboBox.show()

    def verify(self):
        component_creator(
            self.directoryComboBox.currentText(), self.versionComboBox.currentText()
        )
        self.accept()
        return


def show():
    load_plugin_if_needed("bifrostGraph")

    if hasComponentCreatorGraph():
        cmds.warning(f"This scene already contain a {constants.kGraphName} graph")
        return

    dialog = ComponentCreatorDialog(parent=None)
    dialog.exec_()


if __name__ == "__main__":
    show()
