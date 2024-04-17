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
try:
    from PySide2 import QtWidgets
except ModuleNotFoundError:
    from PySide6 import QtWidgets


from bifrost_usd.component_creator.component import find_bifrost_component_graph
from bifrost_usd.component_creator.component import copy_look
from bifrost_usd.component_creator.component import get_model_variant_nodes
from bifrost_usd.component_creator.component import get_look_variant_nodes
from bifrost_usd.component_creator.component import default_model_variant
from bifrost_usd.component_creator.component import default_look_variant

from bifrost_usd.graph_api import GraphAPI


graphAPI = GraphAPI(find_bifrost_component_graph)


class CopyLookDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(CopyLookDialog, self).__init__(parent)

        self.srcModel = default_model_variant()
        self.srcLook = default_look_variant()
        self.tgtModel = default_model_variant()
        self.tgtLook = default_look_variant()

        sourceModelVariantLabel = QtWidgets.QLabel("Source Model Variant")
        self.sourceModelVariantComboBox = self.createSourceModelVariantComboBox()
        self.sourceModelVariantComboBox.currentIndexChanged.connect(self.update)

        sourceLookVariantLabel = QtWidgets.QLabel("Source Look Variant")
        self.sourceLookVariantComboBox = self.createLookVariantComboBox()
        self.sourceLookVariantComboBox.currentIndexChanged.connect(self.update)

        targetModelVariantLabel = QtWidgets.QLabel("Target Model Variant")
        self.targetModelVariantComboBox = self.createSourceModelVariantComboBox()
        self.targetModelVariantComboBox.currentIndexChanged.connect(self.update)

        targetLookVariantLabel = QtWidgets.QLabel("Target Look Variant")
        self.targetLookVariantComboBox = self.createLookVariantComboBox()
        self.targetLookVariantComboBox.currentIndexChanged.connect(self.update)

        mainLayout = QtWidgets.QGridLayout()

        row = 0

        mainLayout.addWidget(sourceModelVariantLabel, row, 0)
        mainLayout.addWidget(self.sourceModelVariantComboBox, row, 1)
        mainLayout.addWidget(targetModelVariantLabel, row, 2)
        mainLayout.addWidget(self.targetModelVariantComboBox, row, 3)
        row += 1

        mainLayout.addWidget(sourceLookVariantLabel, row, 0)
        mainLayout.addWidget(self.sourceLookVariantComboBox, row, 1)
        mainLayout.addWidget(targetLookVariantLabel, row, 2)
        mainLayout.addWidget(self.targetLookVariantComboBox, row, 3)
        row += 1

        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )

        buttonBox.accepted.connect(self.verify)
        buttonBox.rejected.connect(self.reject)

        mainLayout.addWidget(buttonBox, row, 1, 1, 3)

        self.setLayout(mainLayout)

        self.setWindowTitle("Copy Look")
        self.resize(500, 100)

    def createSourceModelVariantComboBox(self):
        comboBox = QtWidgets.QComboBox()
        comboBox.setEditable(False)
        modelVariantNodes = list(dict.fromkeys(get_model_variant_nodes()))
        for node in modelVariantNodes:
            comboBox.addItem(graphAPI.param(node, "geo_variant_name"))

        return comboBox

    def createLookVariantComboBox(self):
        comboBox = QtWidgets.QComboBox()
        comboBox.setEditable(False)
        lookVariantNodes = get_look_variant_nodes()

        names = []
        for node in lookVariantNodes:
            names.append(graphAPI.param(node, "variant_name"))

        for item in list(dict.fromkeys(names)):
            comboBox.addItem(item)

        return comboBox

    def update(self):
        self.srcModel = self.sourceModelVariantComboBox.currentText()
        self.srcLook = self.sourceLookVariantComboBox.currentText()
        self.tgtModel = self.targetModelVariantComboBox.currentText()
        self.tgtLook = self.targetLookVariantComboBox.currentText()

    def verify(self):
        copy_look(self.srcModel, self.srcLook, self.tgtModel, self.tgtLook)
        self.accept()
        return


def show():
    dialog = CopyLookDialog(parent=None)
    status = dialog.exec_()
    if status:
        return dialog


if __name__ == "__main__":
    show()
