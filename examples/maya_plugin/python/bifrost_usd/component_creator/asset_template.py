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
import pathlib
from typing import Any
from typing import Tuple


""" An asset path template used to extract the variant name and purpose of a usd file.
"""

kSupportedFileExtension = (".usd", ".usda", ".usdc", ".abc")


def get_geo_file_info(file_path: str) -> dict[str, str]:
    """Extract the variant name and purpose name from a file path, and
    also the relative path to the component directory.
    """
    fileInfo = {"variant": "default", "purpose": "default", "relative_path": ""}

    if len((pathParts := file_path.split(os.sep))) > 1:
        fileInfo["relative_path"] = os.sep.join(pathParts[-2:])
    else:
        raise ValueError

    fileBaseName = os.path.basename(file_path)
    fileName = os.path.splitext(fileBaseName)[0]

    if len(tokens := fileName.split("_")) == 1:
        fileInfo["variant"] = tokens[0]
        return fileInfo

    if (purpose := fileName.split("_")[-1]) in ("guide", "proxy", "default", "render"):
        fileInfo["purpose"] = purpose
        fileInfo["variant"] = "_".join(fileName.split("_")[:-1])
    else:
        fileInfo["variant"] = fileName

    return fileInfo


class PurposesFilePaths:
    """Stores the (optional) file paths of the supported USD purposes that are
    guide, proxy, default and render
    """

    def __init__(
        self, guide: str = "", proxy: str = "", default: str = "", render: str = ""
    ):
        self.guide = guide
        self.proxy = proxy
        self.default = default
        self.render = render

    def __repr__(self):
        return f"PurposesFilePaths({self.guide}, {self.proxy}, {self.default}, {self.render})"


def get_geo_dir_data(geo_dir_path: str) -> dict:
    """Get all the geo file info for every valid files in a directory.
    A valid file is a file ending with supported extensions.
    Hidden files are ignored (even on non-unix platforms).
    """
    geoDirInfo: dict[str, Any] = {}
    geoFiles = []
    for name in os.listdir(geo_dir_path):
        if name.startswith("."):
            continue

        if pathlib.Path(name).suffix not in (kSupportedFileExtension):
            continue

        if os.path.isfile((filePath := os.path.join(geo_dir_path, name))):
            geoFiles.append(filePath)
            geoFileInfo = get_geo_file_info(filePath)
            purposesFilePaths = geoDirInfo.get(
                geoFileInfo["variant"],
                PurposesFilePaths(),
            )
            if geoFileInfo["purpose"] == "guide":
                purposesFilePaths.guide = geoFileInfo["relative_path"]
            elif geoFileInfo["purpose"] == "proxy":
                purposesFilePaths.proxy = geoFileInfo["relative_path"]
            elif geoFileInfo["purpose"] == "default":
                purposesFilePaths.default = geoFileInfo["relative_path"]
            elif geoFileInfo["purpose"] == "render":
                purposesFilePaths.render = geoFileInfo["relative_path"]

            geoDirInfo[geoFileInfo["variant"]] = purposesFilePaths

    return dict(sorted(geoDirInfo.items()))


def get_model_name_info(value: str) -> Tuple[str, str, str]:
    """ Extract the model name, variant and purpose from the value.
        The name must use camelCase or PascalCase style.
        The variant and purpose must use snake_case style.
        The purpose must be one word without underscores.
    """
    tokens = value.split("_")
    splitCount = len(tokens)
    modelName = ""
    modelVariant = ""
    modelPurpose = ""

    if splitCount == 1:
        modelName = value
        modelVariant = "default"
        modelPurpose = "default"
    elif splitCount == 2:
        modelName = tokens[0]
        modelVariant = tokens[1]
        modelPurpose = "default"
        tokens.append(modelPurpose)

    if splitCount > 1:
        modelName = tokens[0]

        if tokens[-1] == "guide" or tokens[-1] == "proxy" or tokens[-1] == "render":
            modelVariant = "_".join(tokens[1: -1]).lower()
            modelPurpose = tokens[-1].lower()
        else:
            modelVariant = "_".join(tokens[1: ]).lower()
            modelPurpose = "default"

    return modelName, modelVariant, modelPurpose


if __name__ == "__main__":
    pass
