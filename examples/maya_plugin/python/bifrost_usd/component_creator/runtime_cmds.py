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


def component_creator_cmd():
    name = "bifrostUsdRtc_ComponentCreatorUI"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Component Creator",
            annotation="Create a new scene with a Bifrost graph generating a USD component",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator.ui import component_creator_dialog; component_creator_dialog.show()",
            image="USD_generic_200.png",
        )


def refresh_cmd():
    name = "bifrostUsdRtc_Refresh"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Refresh Component",
            annotation="Refresh the USD Component",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator import component; component.re_run_graph()",
            image="execute.png",
        )


def open_materials_in_lookdevx_cmd():
    name = "bifrostUsdRtc_OpenComponentMaterialsInLookdevX"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Open Component Materials in LookdevX Editor",
            annotation="Open every materials of the USD component in the LookdevX Editor",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator import component; component.open_materials_in_lookdevx()",
            image="LookdevX.png",
        )


def create_material_library_cmd():
    name = "bifrostUsdRtc_CreateMaterialLibrary"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Create Material Library",
            annotation="Create a new Material Library file for current Component",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator import component; component.create_material_library()",
            image="material_create.png",
        )


def rename_current_model_variant_cmd():
    name = "bifrostUsdRtc_RenameCurrentModelVariant"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Rename current model variant",
            annotation="Rename current model variant",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator.ui import rename_model_variant_dialog;rename_model_variant_dialog.show()",
        )


def add_model_cmd():
    name = "bifrostUsdRtc_AddModel"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Add a model variant",
            annotation="Add a new model variant",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator.ui import add_model_dialog; add_model_dialog.show()",
            image="object_NEX.png",
        )


def add_look_cmd():
    name = "bifrostUsdRtc_AddLook"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Add Look variant to default Model variant",
            annotation="Add a new Look variant into the default Model variant",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator.ui import add_look_dialog; add_look_dialog.show()",
            image="material_create.png",
        )


def add_new_material_cmd():
    name = "usdModelCmd_AddNewMaterial"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Add new material to Material Library",
            annotation="Add a new material to the Material Library of a USD Component",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator import component; component.assign_new_material_to_selection()",
            image="material_create.png",
        )


def unassign_material_cmd():
    name = "usdModelCmd_UnassignMaterial"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Unassign material on selection",
            annotation="Unassign material on selection",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator import component; component.unassign_material_from_selection()",
            image="material_disconnect.png",
        )


def duplicate_selected_material_cmd():
    name = "usdModelCmd_DuplicateSelectedMaterial"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Duplicate Selected Material in Material Library",
            annotation="Add a material copy from the selection to the Material Library of a USD Component",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator import component; component.duplicate_selected_material()",
            image="material_create.png",
        )


def open_bifrost_graph_editor_cmd():
    name = "bifrostUsdRtc_OpenComponentCreatorGraphEditor"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Open Component Creator in Bifrost Graph Editor ",
            annotation="Open the Component Creator in Bifrost Graph Editor",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator import component; component.open_bifrost_usd_component_graph()",
            image=os.path.join(
                thisDir, "..", "..", "icons", "out_bifrostGraphShape.png"
            ),
        )


def create_set_selection_to_bounds_mode_cmd():
    name = "bifrostUsdRtc_SetSelectionToBoundsMode"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Draw in Bounding Box(es) mode",
            annotation="Draw the selection in Bounding box(es) mode",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator import draw_mode; draw_mode.setSelectionToBoundsMode()",
            image="WireFrame.png",
        )


def create_set_selection_to_inherited_mode_cmd():
    name = "bifrostUsdRtc_SetSelectionToInheritedMode"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Draw as Inherited mode",
            annotation="Draw the selection in Inherited mode",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator import draw_mode; draw_mode.setSelectionToInheritedMode()",
            image="paintJiggle.png",
        )


def show_guide_purposes_cmd():
    name = "bifrostUsdRtc_ShowGuidePurposes"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Show Guide Purposes",
            annotation="Show every Guide Purposes in the scene",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator import purpose; purpose.showGuidePurposes()",
            image="lattice.png",
        )


def show_proxy_purposes_cmd():
    name = "bifrostUsdRtc_ShowProxyPurposes"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Show Proxy Purposes",
            annotation="Show every Proxy Purpose in the scene",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator import purpose; purpose.showProxyPurposes()",
            image="cube.png",
        )


def show_render_purposes_cmd():
    name = "bifrostUsdRtc_ShowRenderPurposes"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Show Render Purposes",
            annotation="Show every Render Purpose in the scene",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator import purpose; purpose.showRenderPurposes()",
            image="sphere.png",
        )


def save_component_cmd():
    name = "bifrostUsdRtc_SaveComponent"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Save Component",
            annotation="Save the USD Component to disk",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator import component; component.save()",
            image="save.png",
        )


def export_geometry_cmd():
    name = "bifrostUsdRtc_ExportGeometry"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Export Selection as USD Geometry layer",
            annotation="Export the selected Maya model as a USD geometry layer",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator.ui import model_export_dialog; model_export_dialog.show()",
            image="save.png",
        )


def add_material_hint_attrib_cmd():
    name = "bifrostUsdRtc_AddMaterialHintAttrib"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Add 'material_hint' attribute to selection.",
            annotation="Add 'material_hint' attribute to selection.",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator.ui import material_hint_dialog; material_hint_dialog.show()",
            image="attributes.png",
        )


def help_cmd():
    name = "bifrostUsdRtc_ComponentCreatorHelp"
    if not cmds.runTimeCommand(name, exists=True):
        cmds.runTimeCommand(
            name,
            default=True,
            label="BifrostUSD: Create Component Help",
            annotation="Quick Help on how to create a USD component",
            tags="BifrostUSD",
            command="from bifrost_usd.component_creator.ui import component_creator_help; component_creator_help.show()",
            image="help.png",
        )


if __name__ == "__main__":
    create_set_selection_to_bounds_mode_cmd()
