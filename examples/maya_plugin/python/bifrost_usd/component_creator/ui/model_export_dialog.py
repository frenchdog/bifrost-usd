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
from bifrost_usd.component_creator.model_exporter import ModelExporter


class ModelExportDialog(QtWidgets.QDialog):
    currentDir = os.getenv(
        "BIFROST_USD_LAB_COMPONENT_ROOT_DIR", cmds.workspace(q=True, dir=True)
    )

    def __init__(self, parent=None):
        super(ModelExportDialog, self).__init__(parent)

        self.isValid = False

        mainLayout = QtWidgets.QVBoxLayout()

        gridLayout = QtWidgets.QGridLayout()

        row = 0

        directoryLabel = QtWidgets.QLabel("Root Directory")
        self.directoryComboBox = self.createDirectoryComboBox(
            ModelExportDialog.currentDir
        )
        self.directoryComboBox.currentIndexChanged.connect(self.update)
        self.browseButton = self.createButton("&Browse...", self.browse)

        gridLayout.addWidget(directoryLabel, row, 0)
        gridLayout.addWidget(self.directoryComboBox, row, 1)
        gridLayout.addWidget(self.browseButton, row, 2)
        row += 1

        checkboxLabel = QtWidgets.QLabel("Resolved from selection")
        self.checkBox = QtWidgets.QCheckBox()
        self.checkBox.setChecked(True)
        self.checkBox.toggled.connect(self.enableSwitch)
        gridLayout.addWidget(checkboxLabel, row, 0)
        gridLayout.addWidget(self.checkBox, row, 1)
        row += 1

        nameLabel = QtWidgets.QLabel("Component Name")
        self.nameLineEdit = QtWidgets.QLineEdit("")
        gridLayout.addWidget(nameLabel, row, 0)
        gridLayout.addWidget(self.nameLineEdit, row, 1)
        row += 1

        purposeLabel = QtWidgets.QLabel("Purpose")
        self.purposeComboBox = self.createPurposeComboBox()
        gridLayout.addWidget(purposeLabel, row, 0)
        gridLayout.addWidget(self.purposeComboBox, row, 1)
        row += 1

        variantLabel = QtWidgets.QLabel("Variant Name")
        self.variantLineEdit = QtWidgets.QLineEdit("default")
        gridLayout.addWidget(variantLabel, row, 0)
        gridLayout.addWidget(self.variantLineEdit, row, 1)
        row += 1

        self.createVersionLabel = QtWidgets.QLabel("Create Version")
        self.createVersionCheckBox = QtWidgets.QCheckBox()
        self.createVersionCheckBox.setChecked(False)
        self.createVersionCheckBox.toggled.connect(self.enableVersion)
        gridLayout.addWidget(self.createVersionLabel, row, 0)
        gridLayout.addWidget(self.createVersionCheckBox, row, 1)
        row += 1

        self.versionLabel = QtWidgets.QLabel("Asset Version")
        self.versionComboBox = self.createVersionComboBox()
        gridLayout.addWidget(self.versionLabel, row, 0)
        gridLayout.addWidget(self.versionComboBox, row, 1)
        row += 1

        okCancelLayout = QtWidgets.QHBoxLayout()
        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )

        buttonBox.accepted.connect(self.verify)
        buttonBox.rejected.connect(self.reject)
        okCancelLayout.addStretch(1)
        okCancelLayout.addWidget(buttonBox)

        mainLayout.addLayout(gridLayout)
        mainLayout.addLayout(okCancelLayout)

        self.setLayout(mainLayout)

        self.setWindowTitle("Export as USD geometry layer")
        self.resize(600, 100)

        self.update()
        self.enableSwitch()

    def createDirectoryComboBox(self, text=""):
        comboBox = QtWidgets.QComboBox()
        comboBox.setEditable(False)
        if text:
            comboBox.addItem(text)
        return comboBox

    def createPurposeComboBox(self):
        comboBox = QtWidgets.QComboBox()
        comboBox.setEditable(False)
        for name in ["default", "guide", "proxy", "render"]:
            comboBox.addItem(name)

        comboBox.setCurrentIndex(0)
        return comboBox

    def createVersionComboBox(self):
        comboBox = QtWidgets.QComboBox()
        comboBox.setEditable(True)
        return comboBox

    def createButton(self, text, member):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(member)
        return button

    def browse(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Select Component Directory",
            ModelExportDialog.currentDir,
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

            ModelExportDialog.currentDir = self.directoryComboBox.currentText()
            self.update()

    def enableSwitch(self):
        isChecked = self.checkBox.isChecked()
        self.nameLineEdit.setDisabled(isChecked)
        self.purposeComboBox.setDisabled(isChecked)
        self.variantLineEdit.setDisabled(isChecked)

    def enableVersion(self):
        if self.createVersionCheckBox.isChecked():
            self.versionLabel.show()
            self.versionComboBox.show()
        else:
            self.versionLabel.hide()
            self.versionComboBox.hide()

    def update(self):
        name, variant, purpose = ModelExporter.get_model_name_info()
        if name:
            self.isValid = True

        self.nameLineEdit.setText(name)
        self.variantLineEdit.setText(variant)

        if purpose == "guide":
            self.purposeComboBox.setCurrentIndex(1)
        elif purpose == "proxy":
            self.purposeComboBox.setCurrentIndex(2)
        elif purpose == "render":
            self.purposeComboBox.setCurrentIndex(3)

        self.versionComboBox.clear()
        assetDir = os.path.join(ModelExportDialog.currentDir, name)
        if os.path.isdir(assetDir):
            if os.path.isfile(os.path.join(assetDir, ".versions")):
                versions = []

                for name in os.listdir(assetDir):
                    if os.path.isfile(os.path.join(assetDir, name)):
                        continue
                    versions.append(name)

                for name in sorted(versions, reverse=True):
                    self.versionComboBox.addItem(name)

                self.versionComboBox.addItem("")
                self.versionLabel.show()
                self.versionComboBox.show()
                self.createVersionCheckBox.setChecked(True)
                self.createVersionCheckBox.setDisabled(True)
                self.createVersionLabel.hide()
                self.createVersionCheckBox.hide()
            else:
                self.versionLabel.hide()
                self.versionComboBox.hide()
        else:
            # The asset dir is not created yet, so there is no versions
            self.versionLabel.hide()
            self.versionComboBox.hide()

    def verify(self):
        exporter = ModelExporter(
            self.directoryComboBox.currentText(),
            model_name=self.nameLineEdit.text(),
            version=self.versionComboBox.currentText(),
            variant=self.variantLineEdit.text(),
            purpose=self.purposeComboBox.currentText(),
            autoNaming=self.checkBox.isChecked(),
        )
        exporter.do()

        # create .versions file if needed
        if self.createVersionCheckBox.isChecked():
            assetDir = os.path.join(exporter.models_dir, exporter.model_name)
            versionsFilePath = os.path.join(assetDir, ".versions")
            if not os.path.exists(versionsFilePath):
                open(versionsFilePath, "a").close()  # noqa:F821

        self.accept()
        return


def show():
    dialog = ModelExportDialog(parent=None)
    if dialog.isValid:
        dialog.exec_()


if __name__ == "__main__":
    show()
