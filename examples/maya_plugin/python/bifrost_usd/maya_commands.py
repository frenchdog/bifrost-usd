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
import maya.api.OpenMaya as om
from maya import cmds

from bifrost_usd import create_stage
from bifrost_usd import author_usd_graph


class BifrostUsdCmd(om.MPxCommand):
    kPluginCmdName = "bifrostUSDExamples"

    kNewStageFlag = "-n"
    kNewStageFlagLong = "-newStage"

    kGrapShapeFlag = "-s"
    kGrapShapeFlagLong = "-shape"

    kOpenStageFlag = "-o"
    kOpenStageFlagLong = "-openStage"

    kFilesFlag = "-f"
    kFilesFlagLong = "-files"

    # Insert node flags
    kInsertNodeFlag = "-i"
    kInsertNodeFlagLong = "-insertNode"

    kCurrentCompoundFlag = "-cc"
    kCurrentCompoundFlagLong = "-currentCompound"

    kNodeSelectionFlag = "-ns"
    kNodeSelectionFlagLong = "-nodeSelection"

    kPortSelectionFlag = "-ps"
    kPortSelectionFlagLong = "-portSelection"

    kNodeTypeFlag = "-nt"
    kNodeTypeFlagLong = "-nodeType"

    kInputPortFlag = "-ip"
    kInputPortFlagLong = "-inputPort"

    kOutputPortFlag = "-op"
    kOutputPortFlagLong = "-outputPort"

    kImportModelToStageFlag = "-im"
    kImportModelToStageFlagLong = "-importModel"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def creator():
        return BifrostUsdCmd()

    @staticmethod
    def createSyntax():
        syntax = om.MSyntax()
        syntax.setObjectType(om.MSyntax.kSelectionList)
        syntax.useSelectionAsDefault(True)
        syntax.addFlag(BifrostUsdCmd.kNewStageFlag, BifrostUsdCmd.kNewStageFlagLong)
        syntax.addFlag(BifrostUsdCmd.kGrapShapeFlag, BifrostUsdCmd.kGrapShapeFlagLong)
        syntax.addFlag(BifrostUsdCmd.kOpenStageFlag, BifrostUsdCmd.kOpenStageFlagLong)
        syntax.addFlag(
            BifrostUsdCmd.kFilesFlag, BifrostUsdCmd.kFilesFlagLong, om.MSyntax.kString
        )
        syntax.addFlag(BifrostUsdCmd.kInsertNodeFlag, BifrostUsdCmd.kInsertNodeFlagLong)
        syntax.addFlag(
            BifrostUsdCmd.kNodeTypeFlag,
            BifrostUsdCmd.kNodeTypeFlagLong,
            om.MSyntax.kString,
        )
        syntax.addFlag(
            BifrostUsdCmd.kCurrentCompoundFlag,
            BifrostUsdCmd.kCurrentCompoundFlagLong,
            om.MSyntax.kString,
        )
        syntax.addFlag(
            BifrostUsdCmd.kNodeSelectionFlag,
            BifrostUsdCmd.kNodeSelectionFlagLong,
            om.MSyntax.kString,
        )
        syntax.addFlag(
            BifrostUsdCmd.kPortSelectionFlag,
            BifrostUsdCmd.kPortSelectionFlagLong,
            om.MSyntax.kString,
        )
        syntax.addFlag(
            BifrostUsdCmd.kInputPortFlag,
            BifrostUsdCmd.kInputPortFlagLong,
            om.MSyntax.kString,
        )
        syntax.addFlag(
            BifrostUsdCmd.kOutputPortFlag,
            BifrostUsdCmd.kOutputPortFlagLong,
            om.MSyntax.kString,
        )

        syntax.addFlag(
            BifrostUsdCmd.kImportModelToStageFlag,
            BifrostUsdCmd.kImportModelToStageFlagLong,
        )

        return syntax

    def doIt(self, args):
        try:
            argdb = om.MArgDatabase(self.syntax(), args)
        except RuntimeError:
            om.MGlobal.displayError(
                "Error while parsing arguments:\n#\t# If passing in list of nodes, also check that node names exist in scene."
            )
            raise

        newStage = argdb.isFlagSet(BifrostUsdCmd.kNewStageFlag)
        asShape = argdb.isFlagSet(BifrostUsdCmd.kGrapShapeFlag)

        openStage = argdb.isFlagSet(BifrostUsdCmd.kOpenStageFlag)

        insertNode = argdb.isFlagSet(BifrostUsdCmd.kInsertNodeFlag)

        importModel = argdb.isFlagSet(BifrostUsdCmd.kImportModelToStageFlag)

        if newStage:
            if importModel:
                currentSelection = cmds.ls(selection=True)
                graph = create_stage.create_new_stage_graph(as_shape=True)

                selection = author_usd_graph.GraphEditorSelection(
                    cmds.ls(selection=True, long=True)[0],  # dgContainerFullPath
                    cmds.ls(selection=True)[0],  # dgContainerName
                    "/",  # currentCompound
                    "stage",  # output
                    ["create_usd_stage"],  # nodeSelection
                )
                addToStageNodeDef = {
                    "type_name": "BifrostGraph,USD::Stage,add_to_stage",
                    "input": "stage",
                    "output": "out_stage",
                }

                selection.nodeSelection = [
                    author_usd_graph.insert_stage_node(selection, addToStageNodeDef)
                ]
                cmds.select(currentSelection, replace=True)
                author_usd_graph.add_maya_selection_to_stage(selection)
                self.setResult(graph)
            else:
                self.setResult(create_stage.create_new_stage_graph(as_shape=asShape))

        elif openStage:
            if argdb.isFlagSet(BifrostUsdCmd.kFilesFlag):
                files = argdb.flagArgumentString(BifrostUsdCmd.kFilesFlag, 0)
                filePaths = files.split(",")
                self.setResult(
                    create_stage.create_graph_from_usd_files(filePaths, as_shape=True)
                )
        elif insertNode:
            dgContainerFullPath = ""
            dgContainerName = ""
            currentCompound = argdb.flagArgumentString(
                BifrostUsdCmd.kCurrentCompoundFlag, 0
            )
            nodeSelection = argdb.flagArgumentString(
                BifrostUsdCmd.kNodeSelectionFlag, 0
            )
            portSelection = argdb.flagArgumentString(
                BifrostUsdCmd.kPortSelectionFlag, 0
            )
            nodeType = argdb.flagArgumentString(BifrostUsdCmd.kNodeTypeFlag, 0)
            inputPort = argdb.flagArgumentString(BifrostUsdCmd.kInputPortFlag, 0)
            outputPort = argdb.flagArgumentString(BifrostUsdCmd.kOutputPortFlag, 0)

            if currentCompound and argdb.getObjectList():
                dgContainerName = argdb.getObjectList().getSelectionStrings()[0]
                dgContainerFullPath = cmds.ls(dgContainerName, long=True)[0]

            if nodeSelection == "":
                nodeSelection = []
            else:
                nodeSelection = [nodeSelection]

            nodeInfo = author_usd_graph.GraphEditorSelection(
                dgContainerFullPath,
                dgContainerName,
                currentCompound,
                portSelection,
                nodeSelection,
            )

            newNodeDef = {
                "type_name": nodeType,
                "input": inputPort,
                "output": outputPort,
            }

            self.setResult(author_usd_graph.insert_stage_node(nodeInfo, newNodeDef))
            return

    def redoIt(self):
        self.dgmod.doIt()

    def undoIt(self):
        self.dgmod.undoIt()

    def isUndoable(self):
        return True
