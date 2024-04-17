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
    from PySide2.QtCore import Qt
    from shiboken2 import wrapInstance
except ModuleNotFoundError:
    from PySide6 import QtWidgets
    from PySide6.QtCore import Qt
    from shiboken6 import wrapInstance

from maya import cmds
from maya import OpenMayaUI as omui

from bifrost_usd.graph_api import bifrost_version


class ComponentCreatorHelp(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ComponentCreatorHelp, self).__init__(parent)

        mainLayout = QtWidgets.QVBoxLayout()

        gridLayout = QtWidgets.QGridLayout()

        row = 0
        bifrostVersionLabel = QtWidgets.QLabel(f"Bifrost version {bifrost_version()}")
        gridLayout.addWidget(bifrostVersionLabel, row, 0)
        row += 1

        bifrostUSDPluginVersion = cmds.pluginInfo("bifrostUSDExamples.py", query=True, version=True)
        bifrostUsdPluginVersionLabel = QtWidgets.QLabel(
            f"BifrostUsd Plugin version {bifrostUSDPluginVersion}"
        )
        gridLayout.addWidget(bifrostUsdPluginVersionLabel, row, 0)
        row += 1

        textEdit = QtWidgets.QTextEdit()
        textEdit.setFrameStyle(QtWidgets.QFrame.NoFrame)
        textEdit.setReadOnly(True)

        dirPath = os.path.dirname(os.path.realpath(__file__))
        textFilePath = os.path.join(dirPath, "component_creator_help.md")
        with open(textFilePath, "r") as file:
            textEdit.setMarkdown(file.read())
        textEdit.setFixedHeight(650)

        gridLayout.addWidget(textEdit, row, 0)
        row += 1

        mainLayout.addLayout(gridLayout)

        closeBtn = QtWidgets.QPushButton("Close", self)
        closeBtn.clicked.connect(self.close)
        mainLayout.addWidget(closeBtn)

        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Component Creator Help")
        self.setFixedWidth(700)
        # self.setFixedHeight(800)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)


def show():
    ptr = omui.MQtUtil.mainWindow()
    widget = wrapInstance(int(ptr), QtWidgets.QWidget)
    dialog = ComponentCreatorHelp(widget)
    dialog.show()


if __name__ == "__main__":
    show()
