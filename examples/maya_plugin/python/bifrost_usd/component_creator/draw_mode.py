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
import ufe
import mayaUsd
from maya import cmds

from pxr import UsdGeom


def setSelectionDrawMode(drawModeValue):
    for item in iter(ufe.GlobalSelection.get()):
        shape_path = item.path().segments[0]
        if (stage := mayaUsd.ufe.getStage(str(shape_path))):
            prim_path = item.path().segments[1]
            prim = stage.GetPrimAtPath(str(prim_path))
            if prim:
                model = UsdGeom.ModelAPI(prim)
                if model:
                    drawMode = model.GetModelDrawModeAttr()
                    drawMode.Set(drawModeValue)
    cmds.ogs(reset=True)


def setSelectionToBoundsMode():
    with mayaUsd.lib.UsdUndoBlock():
        setSelectionDrawMode("bounds")


def setSelectionToInheritedMode():
    with mayaUsd.lib.UsdUndoBlock():
        setSelectionDrawMode("inherited")
