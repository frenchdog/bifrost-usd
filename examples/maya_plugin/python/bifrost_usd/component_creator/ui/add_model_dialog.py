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
from maya import cmds

try:
    from PySide2 import QtWidgets
except ModuleNotFoundError:
    from PySide6 import QtWidgets

from bifrost_usd.component_creator.component import get_geo_dir
from bifrost_usd.component_creator.component import add_model
from bifrost_usd.component_creator.component import hasComponentCreatorGraph


def get_file_from_dialog():
    dlg = QtWidgets.QFileDialog()
    dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)
    filters = ["*.usd", "*.usda", "*.usdc"]
    dlg.setNameFilters(filters)

    if get_geo_dir():
        dlg.setDirectory(get_geo_dir())

    filenames = None
    if dlg.exec_():
        filenames = dlg.selectedFiles()
        if filenames:
            return filenames[0]


class AddModelDialog(QtWidgets.QDialog):
    currentDir = os.getcwd()
    rootDir = None
    modelDir = None
    version = None

    def __init__(self, parent=None):
        super(AddModelDialog, self).__init__(parent)

        self.guidePurposePath = ""
        self.proxyPurposePath = ""
        self.defaultPurposePath = ""
        self.renderPurposePath = ""

        nameLabel = QtWidgets.QLabel("Name")
        self.nameLine = QtWidgets.QLineEdit()

        purposeLabel = QtWidgets.QLabel("Purpose")
        filePathLabel = QtWidgets.QLabel("File Path")

        guidePurposeLabel = QtWidgets.QLabel("Guide Purpose")
        self.guidePurposePath = QtWidgets.QLabel("")
        self.guidePurposeBtn = QtWidgets.QPushButton("...")
        self.guidePurposeBtn.clicked.connect(self.set_guide_file)

        proxyPurposeLabel = QtWidgets.QLabel("Proxy Purpose")
        self.proxyPurposePath = QtWidgets.QLabel("")
        self.proxyPurposeBtn = QtWidgets.QPushButton("...")
        self.proxyPurposeBtn.clicked.connect(self.set_proxy_file)

        defaultPurposeLabel = QtWidgets.QLabel("Default Purpose")
        self.defaultPurposePath = QtWidgets.QLabel("")
        self.defaultPurposeBtn = QtWidgets.QPushButton("...")
        self.defaultPurposeBtn.clicked.connect(self.set_default_file)

        renderPurposeLabel = QtWidgets.QLabel("Render Purpose")
        self.renderPurposePath = QtWidgets.QLabel("")
        self.renderPurposeBtn = QtWidgets.QPushButton("...")
        self.renderPurposeBtn.clicked.connect(self.set_render_file)

        mainLayout = QtWidgets.QGridLayout()
        row = 0

        mainLayout.addWidget(nameLabel, row, 0)
        mainLayout.addWidget(self.nameLine, row, 1)
        row += 1

        mainLayout.addWidget(purposeLabel, row, 0)
        mainLayout.addWidget(filePathLabel, row, 1)
        row += 1

        mainLayout.addWidget(guidePurposeLabel, row, 0)
        mainLayout.addWidget(self.guidePurposePath, row, 1)
        mainLayout.addWidget(self.guidePurposeBtn, row, 2)
        row += 1

        mainLayout.addWidget(proxyPurposeLabel, row, 0)
        mainLayout.addWidget(self.proxyPurposePath, row, 1)
        mainLayout.addWidget(self.proxyPurposeBtn, row, 2)
        row += 1

        mainLayout.addWidget(defaultPurposeLabel, row, 0)
        mainLayout.addWidget(self.defaultPurposePath, row, 1)
        mainLayout.addWidget(self.defaultPurposeBtn, row, 2)
        row += 1

        mainLayout.addWidget(renderPurposeLabel, row, 0)
        mainLayout.addWidget(self.renderPurposePath, row, 1)
        mainLayout.addWidget(self.renderPurposeBtn, row, 2)
        row += 1

        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )

        buttonBox.accepted.connect(self.verify)
        buttonBox.rejected.connect(self.reject)

        mainLayout.addWidget(buttonBox, row, 1, 1, 2)

        self.setLayout(mainLayout)

        self.setWindowTitle("Add Model Variant")
        self.resize(500, 100)

    def set_guide_file(self):
        self.guidePurposePath.setText(get_file_from_dialog())

    def set_proxy_file(self):
        self.proxyPurposePath.setText(get_file_from_dialog())

    def set_default_file(self):
        self.defaultPurposePath.setText(get_file_from_dialog())

    def set_render_file(self):
        self.renderPurposePath.setText(get_file_from_dialog())

    def verify(self):
        add_model(
            self.nameLine.text(),
            guide_geo_file=self.guidePurposePath.text(),
            proxy_geo_file=self.proxyPurposePath.text(),
            default_geo_file=self.defaultPurposePath.text(),
            render_geo_file=self.renderPurposePath.text(),
        )

        self.accept()
        return


def show():
    if hasComponentCreatorGraph() is False:
        cmds.warning("No Component Creator Graph found")
        return

    dialog = AddModelDialog(parent=None)
    status = dialog.exec_()
    if status:
        return dialog


if __name__ == "__main__":
    show()
