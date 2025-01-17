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
from maya import cmds
import os

thisDir = os.path.dirname(os.path.realpath(__file__))


def open_bifrost_usd_graph_editor_cmd():
    name = "bifrostUsdRtc_OpenBifrostUsdGraphEditor"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Open Bifrost Graph Editor from Selected MayaUsdProxyShape",
            annotation="Open Bifrost Graph Editor from Selected USD Prim",
            tags="BifrostUSD",
            command="from bifrost_usd import author_usd_graph; author_usd_graph.open_bifrost_graph_from_prim_selection()",
            image=os.path.join(
                thisDir, "..", "..", "icons", "out_bifrostGraphShape.png"
            ),
        )


def create_new_stage_cmd():
    name = "bifrostUsdRtc_CreateNewStage"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Create New Stage",
            annotation="Creates a stage with a new root layer",
            tags="BifrostUSD",
            command="bifrostUsd -newStage -shape",
            image="USD_generic_200.png",
        )


def create_stage_from_sublayers_cmd():
    name = "bifrostUsdRtc_CreateStageFromSublayers"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Create Stage from Sublayers...",
            annotation="Creates a stage with a new root layer and (read-only) sublayers from files",
            tags="BifrostUSD",
            command="from bifrost_usd.ui import create_from_sublayers_dialog; create_from_sublayers_dialog.show()",
            image="USD_generic_200.png",
        )


if __name__ == "__main__":
    create_stage_from_sublayers_cmd()
