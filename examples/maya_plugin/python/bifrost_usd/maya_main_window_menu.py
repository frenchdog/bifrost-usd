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


def create_usd_menu():
    # Do not need the menu in batch mode.
    if cmds.about(batch=1):
        return

    kTopMenu = "BifrostUSDMenu"

    # Bifrost USD menu
    cmds.menu(kTopMenu, label="Bifrost USD", parent="MayaWindow", tearOff=True)

    # File submenu
    cmds.menuItem(
        "BifrostUSDFileMenu", label="File", parent=kTopMenu, subMenu=True, tearOff=True
    )

    cmds.menuItem(
        "CreateNewStage",
        parent="BifrostUSDFileMenu",
        command="bifrostUSDExamples -newStage -shape",
        label="New Stage",
        sourceType="mel",
        image="USD_generic_200.png",
        tearOff=True,
    )

    cmds.menuItem(
        "CreateStageFromSublayers",
        parent="BifrostUSDFileMenu",
        rtc="bifrostUsdRtc_CreateStageFromSublayers",
        label="Stage From File...",
        sourceType="mel",
        tearOff=True,
    )

    cmds.menuItem(parent="BifrostUSDFileMenu", divider=True, dividerLabel="Component")
    cmds.menuItem(
        "Modeling Export",
        parent="BifrostUSDFileMenu",
        rtc="bifrostUsdRtc_ExportGeometry",
        label="Export Geometry",
        sourceType="mel",
        tearOff=True,
    )

    cmds.menuItem(
        "Save",
        parent="BifrostUSDFileMenu",
        rtc="bifrostUsdRtc_SaveComponent",
        label="Save Component Model",
        sourceType="mel",
        tearOff=True,
    )

    # Edit submenu
    cmds.menuItem(
        "BifrostUSDEditMenu", label="Edit", parent=kTopMenu, subMenu=True, tearOff=True
    )

    cmds.menuItem(
        "InsertSaveStageNode",
        parent="BifrostUSDEditMenu",
        command='bifrostUSDExamples -insertNode -nodeType "BifrostGraph,USD::Stage,save_usd_stage" -currentCompound "" -nodeSelection "" -portSelection "" -inputPort "stage" -outputPort "out_stage"',
        label="Insert Save Stage Node",
        sourceType="mel",
        tearOff=True,
    )
    cmds.menuItem(
        "InsertAddToStageNode",
        parent="BifrostUSDEditMenu",
        command='bifrostUSDExamples -insertNode -nodeType "BifrostGraph,USD::Stage,add_to_stage" -currentCompound "" -nodeSelection "" -portSelection "" -inputPort "stage" -outputPort "out_stage"',
        label="Insert Add to Stage Node",
        sourceType="mel",
        tearOff=True,
    )
    cmds.menuItem(
        "InsertSetPrimActiveNode",
        parent="BifrostUSDEditMenu",
        command='from bifrost_usd import author_usd_graph; author_usd_graph.insert_prim_node(author_usd_graph.GraphEditorSelection("", "", "", "", []), { "type_name": "BifrostGraph,USD::Prim,set_prim_active", "input": "stage", "output": "out_stage" })',
        label="Insert Set Prim Active Node",
        sourceType="python",
        tearOff=True,
    )
    cmds.menuItem(
        "InsertAddVariantSetNode",
        parent="BifrostUSDEditMenu",
        command='from bifrost_usd import author_usd_graph; author_usd_graph.insert_prim_node(author_usd_graph.GraphEditorSelection("", "", "", "", []), { "type_name": "BifrostGraph,USD::VariantSet,add_variant_set", "input": "stage", "output": "out_stage", "prim_path_param_name": "prim_path" })',
        label="Insert Add VariantSet Node",
        sourceType="python",
        tearOff=True,
    )
    cmds.menuItem(
        "InsertAddVariantNode",
        parent="BifrostUSDEditMenu",
        command='from bifrost_usd import author_usd_graph; author_usd_graph.insert_prim_node(author_usd_graph.GraphEditorSelection("", "", "", "", []), { "type_name": "BifrostGraph,USD::VariantSet,add_variant", "input": "stage", "output": "out_stage", "prim_path_param_name": "prim_path" })',
        label="Insert Add Variant Node",
        sourceType="python",
        tearOff=True,
    )
    cmds.menuItem(
        parent="BifrostUSDEditMenu", divider=True, dividerLabel="Import/Export"
    )
    cmds.menuItem(
        "ImportMayaModelToStage",
        parent="BifrostUSDEditMenu",
        command="from bifrost_usd import author_usd_graph; author_usd_graph.add_maya_selection_to_stage()",
        label="Import Maya Model to Stage",
        sourceType="python",
        tearOff=True,
    )

    cmds.menuItem(parent="BifrostUSDEditMenu", divider=True, dividerLabel="Component")
    cmds.menuItem(
        "RenameCurrentModelVariant",
        parent="BifrostUSDEditMenu",
        rtc="bifrostUsdRtc_RenameCurrentModelVariant",
        label="Rename Current Model Variant",
        sourceType="mel",
        tearOff=True,
    )
    cmds.menuItem(
        "UnassignMaterial",
        parent="BifrostUSDEditMenu",
        rtc="usdModelCmd_UnassignMaterial",
        label="Unassign Material",
        sourceType="mel",
        tearOff=True,
    )
    cmds.menuItem(
        "DuplicateSelectedMaterial",
        parent="BifrostUSDEditMenu",
        rtc="usdModelCmd_DuplicateSelectedMaterial",
        label="Duplicate Selected Material",
        sourceType="mel",
        tearOff=True,
    )

    # Create submenu
    cmds.menuItem(
        "BifrostUSDCreateMenu",
        label="Create",
        parent=kTopMenu,
        subMenu=True,
        tearOff=True,
    )

    cmds.menuItem(
        parent="BifrostUSDCreateMenu", divider=True, dividerLabel="Import/Export"
    )
    cmds.menuItem(
        "ImportMayaModelToNewStage",
        parent="BifrostUSDCreateMenu",
        command="bifrostUSDExamples -newStage -importModel",
        label="Create New Stage from Maya selection",
        sourceType="mel",
        tearOff=True,
    )

    cmds.menuItem(parent="BifrostUSDCreateMenu", divider=True, dividerLabel="Component")
    cmds.menuItem(
        "CreateComponentCreatorUI",
        parent="BifrostUSDCreateMenu",
        rtc="bifrostUsdRtc_ComponentCreatorUI",
        label="Component Creator",
        sourceType="mel",
        tearOff=True,
    )

    cmds.menuItem(
        "CreateMaterialLibrary",
        parent="BifrostUSDCreateMenu",
        rtc="bifrostUsdRtc_CreateMaterialLibrary",
        label="Create Material Library",
        sourceType="mel",
        tearOff=True,
    )

    cmds.menuItem(
        "AddLookvariant",
        parent="BifrostUSDCreateMenu",
        rtc="bifrostUsdRtc_AddLook",
        label="Add Look Variant",
        sourceType="mel",
        tearOff=True,
    )
    cmds.menuItem(
        "AddNewMaterial",
        parent="BifrostUSDCreateMenu",
        rtc="usdModelCmd_AddNewMaterial",
        label="Add New Material",
        sourceType="mel",
        tearOff=True,
    )

    cmds.menuItem(
        "BifrostUSDDisplayMenu",
        label="Display",
        parent=kTopMenu,
        subMenu=True,
        tearOff=True,
    )

    cmds.menuItem(
        "ShowPurpose",
        label="Show Purpose...",
        parent="BifrostUSDDisplayMenu",
        subMenu=True,
        tearOff=True,
    )
    cmds.menuItem(
        "Guide",
        parent="ShowPurpose",
        rtc="bifrostUsdRtc_ShowGuidePurposes",
        label="Guide",
        sourceType="mel",
        tearOff=True,
    )
    cmds.menuItem(
        "Proxy",
        parent="ShowPurpose",
        rtc="bifrostUsdRtc_ShowProxyPurposes",
        label="Proxy",
        sourceType="mel",
        tearOff=True,
    )
    cmds.menuItem(
        "Render",
        parent="ShowPurpose",
        rtc="bifrostUsdRtc_ShowRenderPurposes",
        label="Render",
        sourceType="mel",
        tearOff=True,
    )

    cmds.menuItem(
        parent="BifrostUSDDisplayMenu", divider=True, dividerLabel="Component"
    )
    cmds.menuItem(
        "DrawBoundingBoxMode",
        parent="BifrostUSDDisplayMenu",
        rtc="bifrostUsdRtc_SetSelectionToBoundsMode",
        label="Draw in Bounding Box(es) mode",
        sourceType="mel",
        tearOff=True,
    )
    cmds.menuItem(
        "DrawInheritedMode",
        parent="BifrostUSDDisplayMenu",
        rtc="bifrostUsdRtc_SetSelectionToInheritedMode",
        label="Draw as Inherited mode",
        sourceType="mel",
        tearOff=True,
    )

    cmds.menuItem(
        "BifrostUSDModifyMenu",
        label="Modify",
        parent=kTopMenu,
        subMenu=True,
        tearOff=True,
    )
    cmds.menuItem(
        "AddMaterialHintAttrib",
        parent="BifrostUSDModifyMenu",
        rtc="bifrostUsdRtc_AddMaterialHintAttrib",
        label="Add or Modify material_hint Attribute",
        sourceType="mel",
        tearOff=True,
    )

    cmds.menuItem(
        "BifrostUSDWindowsMenu",
        label="Windows",
        parent=kTopMenu,
        subMenu=True,
        tearOff=True,
    )

    cmds.menuItem(
        "Open Bifrost Graph Editor from Selected USD Prim",
        parent="BifrostUSDWindowsMenu",
        rtc="bifrostUsdRtc_OpenBifrostUsdGraphEditor",
        label="Open Bifrost Graph Editor from Selected USD Prim",
        sourceType="mel",
        tearOff=True,
    )

    cmds.menuItem(
        parent="BifrostUSDWindowsMenu", divider=True, dividerLabel="Component"
    )
    cmds.menuItem(
        "Open Component Graph Editor",
        parent="BifrostUSDWindowsMenu",
        rtc="bifrostUsdRtc_OpenComponentCreatorGraphEditor",
        label="Open Component Creator Graph Editor",
        sourceType="mel",
        tearOff=True,
    )
    cmds.menuItem(
        "Open Component Material(s) Editor",
        parent="BifrostUSDWindowsMenu",
        rtc="bifrostUsdRtc_OpenComponentMaterialsInLookdevX",
        label="Open Component Materials in LookdevX Graph Editor",
        sourceType="mel",
        tearOff=True,
    )
    cmds.menuItem(
        "Rebuild",
        parent=kTopMenu,
        rtc="bifrostUsdRtc_Refresh",
        label="Re-run Bifrost Graph",
        sourceType="mel",
        tearOff=True,
    )
    cmds.menuItem(parent=kTopMenu, divider=True)

    cmds.menuItem(
        "BifrostUSDHelpMenu", label="Help", parent=kTopMenu, subMenu=True, tearOff=True
    )

    cmds.menuItem(
        "CreateComponentHelp",
        parent="BifrostUSDHelpMenu",
        rtc="bifrostUsdRtc_ComponentCreatorHelp",
        label="Component Creator",
        sourceType="mel",
        tearOff=True,
    )


if __name__ == "__main__":
    create_usd_menu()
