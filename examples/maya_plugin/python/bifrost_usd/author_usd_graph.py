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
from typing import Dict, List
from dataclasses import dataclass

from maya import cmds
import ufe

from bifrost_usd.constants import (
    kDefinePrimHierarchy,
    kMayaUsdProxyShape,
    kBifrostBoard,
    kBifrostGraphShape,
)

from bifrost_usd.graph_api import GraphAPI


def log(args):
    pass
    # print(args)


def find_bifrost_usd_graph() -> str:
    for graph in cmds.ls(type="bifrostGraphShape"):
        if "USDWorkflow" in cmds.listAttr(graph):
            return graph

    return ""


def has_bifrost_usd_graph() -> bool:
    if find_bifrost_usd_graph():
        return True
    return False


graphAPI = GraphAPI(find_bifrost_usd_graph)


@dataclass
class GraphEditorSelection:
    dgContainerFullPath: str
    dgContainerName: str
    currentCompound: str
    output: str
    nodeSelection: List


def get_graph_editor_selection() -> GraphEditorSelection:
    """Get the DG container, the current compound (that the graph editor is viewing)
    and the current node selection in this compound.
    """
    selection = GraphEditorSelection("", "", "", "", [])
    try:
        cmds.refresh(force=True)
        rtn = cmds.vnnCompoundEditor(
            query=True, dgContainer=True, currentCompound=True, nodeSelection=True
        )

        selection.dgContainerFullPath = rtn[0]
        selection.dgContainerName = rtn[0].split("|")[-1]
        selection.currentCompound = rtn[1]

        if len(rtn) == 2:
            selection.nodeSelection = []
        elif len(rtn) == 3:
            selection.nodeSelection = [rtn[-1]]
        else:
            selection.nodeSelection = rtn[(len(rtn) - 2) :]

    except RuntimeError:
        cmds.error("You need to open a Bifrost Graph.")

    return selection


@dataclass
class StagePortData:
    node: str
    port: str


def get_connected_stage_port(
    graph_name: str, current_compound: str, node_name: str
) -> StagePortData:
    """Find the node downstream with an input port connected to the output of the "stage node".
    A "stage node" is a node with an output port named "out_stage" or "stage".
    """
    if not (rtn := graphAPI.connexions(node_name, "out_stage", graph_name)):
        rtn = graphAPI.connexions(node_name, "stage", graph_name)

    stagePortData = StagePortData("", "")
    if rtn:
        stagePortData.node = rtn[0].split(".")[0]
        stagePortData.port = rtn[0].split(".")[1]

    return stagePortData


def insert_stage_node(graph_selection: GraphEditorSelection, new_node_def: dict) -> str:
    """Insert a node downstream of the selected node.

    :return: The inserted node.
    """
    sel = graph_selection
    if not sel.nodeSelection:
        # keep the port name since it can't be deduced from the selection.
        output = sel.output
        sel = get_graph_editor_selection()
        if not sel.nodeSelection:
            cmds.warning(
                "You must select a node upstream (with a stage output) in the Bifrost Graph Editor"
            )
            return ""

        sel.output = output

    srcNode = sel.nodeSelection[0]

    # no explicit output, then take last output of the node.
    if not sel.output:
        if connectedPorts := graphAPI.connected_ports(srcNode):
            # assume there is only one connected output
            # TODO: Add query of port type to vnnNode command.
            output = connectedPorts[-1]
            sel.output = output.split(".")[-1]
        else:
            cmds.warning("Selected node is not connected")
            return ""

    if not sel.output:
        cmds.warning("Selected node is not connected")
        return ""

    if not (
        newNode := graphAPI.add_node(
            new_node_def["type_name"],
            current_compound=sel.currentCompound,
        )
    ):
        # if there is no new node, Maya should print an error.
        return ""

    # store the connection info of source node before connecting it to a new node downstream
    cnxInfo = get_connected_stage_port(
        sel.dgContainerFullPath, sel.currentCompound, srcNode
    )

    # Connect output of source node to input of new node
    graphAPI.connect(srcNode, sel.output, newNode, new_node_def["input"])

    # Connect output of new node to input of node connected to source node
    if cnxInfo.node == sel.dgContainerName:
        graphAPI.connect(newNode, new_node_def["output"], "", cnxInfo.port)
    else:
        newNodeName = cnxInfo.node
        graphAPI.connect(newNode, new_node_def["output"], newNodeName, cnxInfo.port)

    return newNode


# TODO: add test
def insert_prim_node(graph_selection: GraphEditorSelection, new_node_def: dict) -> str:
    primPath = ""
    sel = cmds.ls(selection=True, ufe=True)
    if sel:
        primPath = sel[0].split(",")[-1]

    if not primPath:
        cmds.warning("Please select a USD prim")

    newNode = insert_stage_node(graph_selection, new_node_def)
    info = get_graph_editor_selection()

    primPathParamName = new_node_def.get("prim_path_param_name", "path")

    graphAPI.set_param(
        newNode, (primPathParamName, primPath), current_compound=info.currentCompound
    )
    return newNode


def _get_maya_paths_from_selection() -> tuple[list, list]:
    meshesPaths = []
    leafPaths = []

    def _get_children(node, paths):
        children = cmds.listRelatives(node, type="transform", fullPath=True)
        if children:
            paths += children
            for child in children:
                _get_children(child, paths)

        return paths

    transformList = cmds.ls(type="transform", selection=True, long=True)
    if not transformList:
        cmds.warning("Please select a Maya transform node")

    for transform in transformList:
        paths: list = []
        _get_children(transform, paths)

        for item in paths:
            meshes = cmds.listRelatives(
                item, type="mesh", noIntermediate=True, fullPath=True
            )
            if meshes:
                meshesPaths += meshes
            else:
                if not cmds.listRelatives(
                    item, allDescendents=True, noIntermediate=True
                ):
                    leafPaths.append(item)

    if not meshesPaths:
        for transform in cmds.ls(type="transform", selection=True, long=True):
            # listRelatives can returns None in python
            rtn = cmds.listRelatives(
                transform, type="mesh", noIntermediate=True, fullPath=True
            )

            if rtn:
                meshesPaths += rtn

    return meshesPaths, leafPaths


def _get_connected_add_to_stage(node_name: str) -> str:
    addToStageNode = ""
    if nodes := graphAPI.connexions(node_name):
        for node in nodes:
            if graphAPI.type_name(node) == "BifrostGraph,USD::Stage,add_to_stage":
                addToStageNode = node
                break

    return addToStageNode


def resolve_prim_path(
    dg_container: str, add_to_stage_path: str, prim_path: str
) -> tuple[str, str]:
    """When a "define prim" compound is connected to an add_to_stage compound with its 'parent_path' parameter set to
    a value not equal to "/" or to an empty string, the value of its 'path' parameter should be relative to the 'parent_path'.


    :param: dg_container The Maya dag path
    :param: add_to_stage_path The 'add_to_stage' compound path
    :param: prim_path The full path of the prim

    :return: The parent path and the path without the parent path.
    """

    primPath = prim_path
    parentPath = graphAPI.param(add_to_stage_path, "parent_path")
    parentPartsLenght = len(parentPath.split("/"))
    if parentPath and parentPath != "/":
        primPath = "/" + "/".join(prim_path.split("/")[parentPartsLenght:])

    return parentPath, primPath


def _add_maya_mesh_to_stage(
    mesh_path: str,
    info: GraphEditorSelection,
    add_to_stage_path: str,
    index: int,
    mergeTransformAndShape=True,
) -> None:
    ioNode = cmds.vnnCompound(
        info.dgContainerFullPath, info.currentCompound, addIONode=True
    )[0]

    # TODO: vnn command renaming a node should return the new name.
    ioNodeName = "Input_by_Path_USD" + str(index)
    suffix = str(index)
    while ioNodeName in find_all_input_by_path_nodes():
        suffix += str(index)
        ioNodeName += suffix

    meshName = "mesh" + suffix

    graphAPI.rename_node(ioNode, ioNodeName)

    pathInfo = "pathinfo={path=" + mesh_path + ";setOperation=+;active=true}"
    graphAPI.create_output_port(ioNodeName, (meshName, "Object"), pathInfo)
    graphAPI.set_metadata(ioNodeName, ("bifrostUSD", "input_by_path"))
    graphAPI.create_input_port(
        add_to_stage_path, (f"prim_definitions.mesh{suffix}", "auto")
    )

    defineHierarchy = graphAPI.add_node(kDefinePrimHierarchy)
    graphAPI.connect(
        src_node=defineHierarchy,
        out_port="prim_definitions",
        target_node=add_to_stage_path,
        in_port=f"prim_definitions.mesh{suffix}",
    )

    primPath = mesh_path.replace("|", "/")
    if mergeTransformAndShape:
        primPath = "/".join(primPath.split("/")[:-1])

    parentPath, primPath = resolve_prim_path(
        info.dgContainerFullPath, add_to_stage_path, primPath
    )

    graphAPI.set_param(defineHierarchy, ("path", primPath))
    graphAPI.set_param(defineHierarchy, ("parent_is_scope", "1" if parentPath else "0"))

    # TODO: Use graphAPI
    cmds.vnnConnect(
        info.dgContainerFullPath, f".{meshName}", f"/{defineHierarchy}.leaf_mesh"
    )

    # collapse node
    graphAPI.set_metadata(defineHierarchy, ("DisplayMode", "1"))


def _add_maya_leaf_xform_to_stage(
    xform_path: str,
    info: GraphEditorSelection,
    add_to_stage_path: str,
    index: int,
) -> None:
    suffix = str(index)
    cmds.vnnNode(
        info.dgContainerFullPath,
        add_to_stage_path,
        createInputPort=(f"prim_definitions.xform{suffix}", "auto"),
    )

    defineHierarchy = cmds.vnnCompound(
        info.dgContainerFullPath,
        info.currentCompound,
        addNode=kDefinePrimHierarchy,
    )[0]

    cmds.vnnConnect(
        info.dgContainerFullPath,
        f"/{defineHierarchy}.prim_definitions",
        f"{add_to_stage_path}.prim_definitions.xform{suffix}",
    )

    primPath = xform_path.replace("|", "/")
    _, primPath = resolve_prim_path(
        info.dgContainerFullPath, add_to_stage_path, primPath
    )

    cmds.vnnNode(
        info.dgContainerFullPath,
        f"/{defineHierarchy}",
        setPortDefaultValues=(
            "path",
            primPath,
        ),
    )


def _add_maya_selection_to_stage(info: GraphEditorSelection, add_to_stage_path: str):
    meshSelection, xfoLeafSelection = _get_maya_paths_from_selection()
    for index, meshPath in enumerate(meshSelection):
        index += 1
        _add_maya_mesh_to_stage(meshPath, info, add_to_stage_path, index)

    for index, xfoPath in enumerate(xfoLeafSelection):
        index += 1
        _add_maya_leaf_xform_to_stage(xfoPath, info, add_to_stage_path, index)


def add_maya_selection_to_stage(selection=None) -> bool:
    if not selection:
        selection = get_graph_editor_selection()

    if not (nodeSelection := selection.nodeSelection):
        cmds.warning("Please select a add_to_stage compound")
        return False

    srcNode = nodeSelection[0]
    if graphAPI.type_name(srcNode) != "BifrostGraph,USD::Stage,add_to_stage":
        cmds.warning("Please select a add_to_stage compound")
        return False

    runOnDemandValue = cmds.getAttr(f"{selection.dgContainerFullPath}.runOnDemand")
    try:
        # Disable graph while connecting nodes to avoid fan-in port error messages.
        cmds.setAttr(f"{selection.dgContainerFullPath}.runOnDemand", True)
        _add_maya_selection_to_stage(selection, selection.currentCompound + srcNode)
        pass
    except Exception as e:
        raise e

    cmds.setAttr(f"{selection.dgContainerFullPath}.runOnDemand", runOnDemandValue)
    return True


def find_all_prim_paths(
    node_type: str = kDefinePrimHierarchy,
) -> list[str]:
    paths = []
    for node in graphAPI.find_nodes(node_type):
        paths.append(graphAPI.param(node, "path"))

    return paths


def find_all_input_by_path_nodes() -> list[str]:
    """TODO: Remove this workaround to retrieve input by path nodes"""
    allNodes = cmds.vnnCompound(graphAPI.name, "/", listNodes=True)

    inputByPathNodes = []
    for node in allNodes:
        rtn = cmds.vnnNode(graphAPI.name, f"/{node}", queryMetaData="bifrostUSD")
        if rtn and rtn[0] == "input_by_path":
            inputByPathNodes.append(node)

    return inputByPathNodes


def is_new_path_a_parent(path: str, new_path: str) -> bool:
    log(f"[is_new_path_a_parent]: args: path: {path}, new_path: {new_path}")

    pathTokens = path.split("/")
    newPathTokens = new_path.split("/")

    if newPathTokens[-1] == pathTokens[-1]:
        return True

    return False


def rename_nodes_path_parameter(
    old_prim_path: str, new_prim_path: str, node_type: str = kDefinePrimHierarchy
) -> None:
    allNodes = graphAPI.find_nodes(node_type)
    if allNodes:
        log(f"[rename_nodes_path_parameter] args: {old_prim_path} to {new_prim_path}")

    for node in allNodes:
        rename_path_parameter(node, old_prim_path, new_prim_path)


def rename_path_parameter(node: str, old_prim_path: str, new_prim_path: str) -> None:
    """If the path parameter value of the node is equal to the old prim path, replace it by the new one."""
    pathValue = graphAPI.param(node, "path")
    addToStageNode = _get_connected_add_to_stage(node)

    parentPath, oldPrimPath = resolve_prim_path(
        graphAPI.name, f"/{addToStageNode}", old_prim_path
    )

    _, newPrimPath = resolve_prim_path(
        graphAPI.name, f"/{addToStageNode}", new_prim_path
    )

    log(
        f"[rename_path_parameter] args({old_prim_path}, {new_prim_path}). pathValue: {pathValue} TRY TO REPLACE {oldPrimPath} with {newPrimPath}"
    )
    if pathValue.startswith(oldPrimPath):
        newPath = pathValue.replace(oldPrimPath, newPrimPath)
        log(f"[rename_path_parameter] PATH REPLACED BY {newPath}")
        graphAPI.set_param(node, ("path", newPath))


def reparent_nodes_path_parameter(
    old_prim_path: str, new_prim_path: str, node_type: str = kDefinePrimHierarchy
) -> None:
    allNodes = graphAPI.find_nodes(node_type)
    if allNodes:
        log(f"[reparent_nodes_path_parameter] from {old_prim_path} to {new_prim_path}")

    for node in allNodes:
        log(f"[reparent_nodes_path_parameter]     node {node}")
        reparent_path_parameter(node, old_prim_path, new_prim_path)


def reparent_path_parameter(node: str, old_prim_path: str, new_prim_path: str) -> None:
    """If the path parameter value of the node is equal to the old prim path, replace it by the new one
    if it is a valid reparent path."""
    pathValue = graphAPI.param(node, "path")
    log(f"[reparent_nodes_path_parameter]         pathValue {pathValue}")

    addToStageNode = _get_connected_add_to_stage(node)

    if not addToStageNode:
        return

    parentPath, newPrimPath = resolve_prim_path(
        graphAPI.name, f"/{addToStageNode}", new_prim_path
    )

    if not parentPath and is_new_path_a_parent(pathValue, new_prim_path):
        newPath = pathValue.replace(pathValue, newPrimPath)
        log(f"[reparent_nodes_path_parameter]                 NEW PATH {newPath}")
        graphAPI.set_param(node, ("path", newPath))
        return


def delete_node(old_prim_path: str, node_type: str) -> None:
    def _delete(node: str) -> bool:
        pathValue = cmds.vnnNode(
            graphAPI.name, f"/{node}", queryPortDefaultValues="path"
        )

        addToStage = _get_connected_add_to_stage(node)

        parentPath, oldPrimPath = resolve_prim_path(
            graphAPI.name, f"/{addToStage}", old_prim_path
        )

        if oldPrimPath == "/":
            return False

        if pathValue == oldPrimPath:
            if graphAPI.connexions(node, "leaf_mesh"):
                for ibp in find_all_input_by_path_nodes():
                    if cnx := graphAPI.connexions(ibp):
                        if cnx[0] == node:
                            graphAPI.remove_node(node)
                            graphAPI.remove_node(ibp)
            else:
                graphAPI.remove_node(node)

            return True

        return False

    for node in graphAPI.find_nodes(node_type):
        if _delete(node):
            break


def belong_to_maya_model(ufe_path_str: str) -> bool:
    # remove |world prefix.
    ufeToMayaPath = ufe_path_str[6:]

    for prim_path in find_all_prim_paths():
        primToMayaPath = prim_path.replace("/", "|")
        if cmds.ls(primToMayaPath, long=True):
            if primToMayaPath == ufeToMayaPath:
                return True

    return False


def is_supported_prim_type(ufe_path_str: str) -> bool:
    ufePath = ufe.PathString.path(ufe_path_str)
    ufeItem = ufe.Hierarchy.createItem(ufePath)

    # if the item is directly under "|world" there is no UFE item
    if not ufeItem:
        # remove |world prefix.
        if cmds.ls(ufe_path_str[6:], type="transform"):
            return True

    if ufeItem and ufeItem.nodeType() in ["transform", "mesh"]:
        return True

    return False


def to_prim_path(ufe_path: str) -> str:
    """Convert an UFE absolute path to the value stored in the path
    parameter of a "define prim" compound. If the UFE path point to a mesh
    the shape part of the path is removed."""
    if (ufe_path == "|world|") or (not ufe_path.startswith("|world|")):
        return ""

    mayaPath = "|" + "|".join(ufe_path.split("|")[2:])

    # Since we merge transfrom and shape on Bifrost side,
    # remove last name of te path if it is a mesh
    if cmds.ls(mayaPath, type="mesh"):
        mayaPath = "|".join(mayaPath.split("|")[:-1])

    primPath = mayaPath.replace("|", "/")
    return primPath


def get_prim_selection() -> Dict[str, List[str]]:
    """Get the selected prims in a MayaUsdProxyShape.

    Returns a dictionary of MayaUsdProxyShape's name to USD prim's paths.
    """

    selection: Dict[str, List[str]] = {}

    pathList: List[str] = cmds.ls(
        selection=True, type=kMayaUsdProxyShape, ufeObjects=True
    )

    for path in pathList:
        shapeAndPrim = path.split(",")
        if len(shapeAndPrim) > 1:
            node, prim = shapeAndPrim
            selection[node] = selection.get(node, []) + [prim]

    if not selection:
        cmds.warning("No Usd Prim selected")

    return selection


def open_bifrost_usd_graph() -> None:
    if cmds.about(batch=1):
        return

    if graph := find_bifrost_usd_graph():
        cmds.vnnCompoundEditor(
            name="bifrostGraphEditorControl",
            title="Bifrost Graph Editor",
            edit=graph,
        )


def get_bifrost_graph_from_prim_selection() -> tuple[str, str]:
    """Get the Bifrost graph connected to the MayaUsdProxyShape of the selected USD prim.

    Returns the name of the graph and the name of the output port of the graph.
    """
    if not (selection := get_prim_selection()):
        cmds.warning("No Usd Prim selected")
    else:
        usdProxyShape = list(selection.keys())[0]
        assert cmds.nodeType(usdProxyShape) == kMayaUsdProxyShape

        def get_bifrost_connection_info(
            usdProxyShape: str, bifrostNodeType: str
        ) -> tuple[str, str]:
            if cmds.listConnections(usdProxyShape, type=bifrostNodeType):
                connectionsPlugs = cmds.listConnections(
                    usdProxyShape, type=bifrostNodeType, plugs=True
                )
                if connectionsPlugs:
                    return connectionsPlugs[0].split(".")

            return ("", "")

        graph, plug = get_bifrost_connection_info(usdProxyShape, kBifrostBoard)
        if not graph:
            graph, plug = get_bifrost_connection_info(usdProxyShape, kBifrostGraphShape)

        return graph, plug

    return ("", "")


def open_bifrost_graph_from_prim_selection() -> None:
    graph = get_bifrost_graph_from_prim_selection()[0]
    if graph:
        cmds.vnnCompoundEditor(
            name="bifrostGraphEditorControl",
            title="Bifrost Graph Editor",
            edit=graph,
        )
        return


if __name__ == "__main__":
    open_bifrost_usd_graph()
