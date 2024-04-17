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

from bifrost_usd.constants import (
    kBifrostBoard,
    kBifrostGraphShape,
    kConstantString,
    kCreateUsdStage,
    kDefaultLayerIdentifier,
    kGraphName,
    kMayaUsdProxyShape,
    kOpenStage,
    kOpenUsdLayer,
    kSceneInfo,
    kStringJoin,
)

from bifrost_usd.author_usd_graph import find_bifrost_usd_graph, open_bifrost_usd_graph


def _create_empty_graph(as_shape: bool) -> str:
    """Create an new Bifrost graph without input node.

    :param as_shape: To create a bifrostGraphShape or a bifrostBoard node.
    :returns:       The name of the new graph.
    """
    if graph := find_bifrost_usd_graph():
        cmds.warning(f"{graph} graph is already in this scene")
        return graph

    if not graph:
        graph = cmds.createNode(kBifrostGraphShape if as_shape else kBifrostBoard)

    if as_shape:
        transform = cmds.listRelatives(graph, parent=True, fullPath=True)[0]
        transform = cmds.rename(transform, kGraphName)
        graph = cmds.listRelatives(transform)[0]
    else:
        graph = cmds.rename(graph, kGraphName)

    cmds.addAttr(
        graph,
        shortName="usdw",
        longName="USDWorkflow",
        attributeType="bool",
        defaultValue=True,
        hidden=True,
    )

    cmds.vnnCompound(graph, "/", removeNode="input")
    return graph


def _set_shared_stage(graph: str, value: bool) -> None:
    connections = cmds.listConnections(graph, type=kMayaUsdProxyShape)
    if connections:
        usdProxyShape = connections[0]
        cmds.setAttr(f"{usdProxyShape}.shareStage", value)


def _output_stage_to_maya(graph: str, node: str) -> str:

    graphAttribs = cmds.listAttr(graph, readOnly=True, scalar=True, fromPlugin=True)
    hasStageOutput = False
    if graphAttribs:
        if "stage" in graphAttribs:
            hasStageOutput = True

    if not hasStageOutput:
        cmds.vnnNode(
            graph,
            "/output",
            createInputPort=("stage", "BifrostUsd::Stage"),
        )

    cmds.vnnConnect(
        graph,
        f"/{node}.stage",
        ".stage",
    )

    _set_shared_stage(graph, False)
    return graph


def create_new_stage_graph(as_shape: bool = True) -> str:
    """Creates a stage with a new root layer and output it from the graph.

    :param as_shape: To create a bifrostGraphShape or a bifrostBoard node.
    :returns:       The name of the new graph.
    """

    if graph := find_bifrost_usd_graph():
        cmds.warning(f"{graph} already in this scene")
        return graph

    graph = _create_empty_graph(as_shape)
    createStageNode = cmds.vnnCompound(graph, "/", addNode=kCreateUsdStage)[0]

    cmds.vnnNode(
        graph,
        f"/{createStageNode}",
        setPortDefaultValues=("layer", kDefaultLayerIdentifier),
    )

    _output_stage_to_maya(graph, createStageNode)

    open_bifrost_usd_graph()

    return graph


def _as_relative_path(file_path):
    result = file_path
    scenePath = cmds.file(query=True, sceneName=True)
    if scenePath:
        dirPath = os.path.dirname(scenePath)
        result = os.path.relpath(file_path, dirPath)
    else:
        result = file_path

    return result


def _create_sublayers_loader_graph(
    graph: str, file_paths: list[str], relative_path=True
) -> None:
    """Creates a stage with a new root layer and (read-only) sublayers from files.
    The resulting stage is the output of the graph."""
    createStageNode = cmds.vnnCompound(graph, "/", addNode=kCreateUsdStage)[0]

    relativePath = cmds.file(query=True, sceneName=True) and relative_path
    if relativePath:
        sceneInfoNode = cmds.vnnCompound(graph, "/", addNode=kSceneInfo)[0]

    cmds.vnnNode(
        graph,
        f"/{createStageNode}",
        setPortDefaultValues=("layer", kDefaultLayerIdentifier),
    )

    i = ""
    for fpath in file_paths:
        openLayerNode = cmds.vnnCompound(graph, "/", addNode=kOpenUsdLayer)[0]
        cmds.vnnNode(graph, f"/{openLayerNode}", setMetaData=("DisplayMode", "1"))

        if relativePath:
            stringJoinNode = cmds.vnnCompound(graph, "/", addNode=kStringJoin)[0]
            cmds.vnnNode(graph, f"/{stringJoinNode}", setMetaData=("DisplayMode", "1"))
            cmds.vnnNode(
                graph, f"/{stringJoinNode}", setPortDefaultValues=("separator", "")
            )
            # enable fan-in on strings input port
            cmds.vnnPort(graph, f"/{stringJoinNode}.strings", 0, 1, set=2)

            # connect scene_info to string_join
            cmds.vnnNode(
                graph,
                f"/{stringJoinNode}",
                createInputPort=("strings.scene_directory", "string"),
            )
            cmds.vnnConnect(
                graph,
                f"/{sceneInfoNode}.scene_directory",
                f"/{stringJoinNode}.strings.scene_directory",
            )

            valueNode = cmds.vnnCompound(graph, "/", addNode=kConstantString)[0]
            cmds.vnnNode(graph, f"/{valueNode}", setMetaData=("DisplayMode", "1"))
            cmds.vnnNode(
                graph,
                f"/{valueNode}",
                setPortDefaultValues=("value", _as_relative_path(fpath)),
            )

            cmds.vnnNode(
                graph,
                f"/{stringJoinNode}",
                createInputPort=("strings.relative_path", "string"),
            )
            cmds.vnnConnect(
                graph,
                f"/{valueNode}.output",
                f"/{stringJoinNode}.strings.relative_path",
            )

            cmds.vnnConnect(
                graph, f"/{stringJoinNode}.joined", f"/{openLayerNode}.file"
            )

        cmds.vnnNode(
            graph,
            f"/{openLayerNode}",
            setPortDefaultValues=("file", fpath),
        )

        cmds.vnnNode(
            graph,
            f"/{createStageNode}",
            createInputPort=(f"sublayers.layer{i}", "auto"),
        )

        cmds.vnnConnect(
            graph,
            f"/{openLayerNode}.layer",
            f"/{createStageNode}.sublayers.layer{i}",
        )

        i = str(int(i) + 1) if i else "1"

    # Output stage to Maya
    cmds.vnnNode(
        graph,
        "/output",
        createInputPort=("stage", "BifrostUsd::Stage"),
    )
    cmds.vnnConnect(
        graph,
        f"/{createStageNode}.stage",
        ".stage",
    )

    _set_shared_stage(graph, False)


def _create_open_stage_graph(graph: str, file_path: str) -> None:
    """Creates a stage from a USD file and output it from the graph."""
    openStageNode = cmds.vnnCompound(graph, "/", addNode=kOpenStage)[0]

    cmds.vnnNode(
        graph,
        f"/{openStageNode}",
        setPortDefaultValues=("file", file_path),
    )

    _output_stage_to_maya(graph, openStageNode)


def create_graph_from_usd_files(file_paths: list[str], as_shape: bool) -> str:
    if not file_paths:
        cmds.warning("No file paths found")
        return ""

    graph = _create_empty_graph(as_shape=as_shape)

    if len(file_paths) == 1:
        _create_open_stage_graph(graph, file_paths[0])
    elif len(file_paths) > 1:
        _create_sublayers_loader_graph(graph, file_paths)

    open_bifrost_usd_graph()

    return graph


if __name__ == "__main__":
    pass
