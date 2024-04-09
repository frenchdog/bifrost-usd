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
import unittest

from maya import cmds
from maya import standalone

from bifrost_usd import create_stage
from bifrost_usd import author_usd_graph


from bifrost_usd.constants import (
    kBifrostBoard,
    kBifrostGraphShape,
    kGraphName,
    kMayaUsdProxyShape,
)


class BifrostStageCmdsTestCase(unittest.TestCase):
    plugins_loaded = False

    @classmethod
    def setUpClass(cls):
        if not cls.plugins_loaded:
            standalone.initialize("bifrost-usd-create-stage-cmds")
            cmds.loadPlugin("mayaUsdPlugin", quiet=True)
            cmds.loadPlugin("bifrostGraph", quiet=True)
            cmds.loadPlugin("bifrostUSDExamples.py", quiet=True)
            cls.plugins_loaded = True

    @classmethod
    def tearDownClass(cls):
        standalone.uninitialize()

    def setUp(self):
        cmds.file(f=True, new=True)

    def testCreateEmptyGraphShape(self):
        graph = create_stage._create_empty_graph(as_shape=True)
        self.assertEqual(cmds.nodeType(graph), kBifrostGraphShape)
        self.assertEqual(graph, f"{kGraphName}Shape")

    def testCreateEmptyGraphBoard(self):
        graph = create_stage._create_empty_graph(as_shape=False)
        self.assertEqual(cmds.nodeType(graph), kBifrostBoard)
        self.assertEqual(graph, kGraphName)

    def testCreateNewStageGraph(self):
        graph = create_stage.create_new_stage_graph()
        self.assertEqual(cmds.nodeType(graph), kBifrostGraphShape)
        self.assertTrue("stage" in cmds.listAttr(graph, scalar=True))

    def testCreateNewBoardStageCommand(self):
        # create a bifrostBoard node
        graph = cmds.bifrostUSDExamples(newStage=True)
        self.assertEqual(graph, [kGraphName])
        self.assertEqual(cmds.nodeType(graph[0]), kBifrostBoard)
        self.assertTrue("stage" in cmds.listAttr(graph, scalar=True))

    def testCreateNewShapeStageCommand(self):
        # no mayaUsdProxyShape should be there
        self.assertFalse(cmds.ls(type=kMayaUsdProxyShape))

        # create a bifrostGraphShape node
        graph = cmds.bifrostUSDExamples(newStage=True, shape=True)
        self.assertEqual(graph, [f"{kGraphName}Shape"])
        self.assertEqual(cmds.nodeType(graph[0]), kBifrostGraphShape)
        self.assertTrue("stage" in cmds.listAttr(graph, scalar=True))

        # a mayaUsdProxyShape should be there
        self.assertTrue(cmds.ls(type=kMayaUsdProxyShape))

    def testCreateGraphFromUsdFile(self):
        filePath = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "resources", "capsule.usd"
        )
        self.assertTrue(os.path.isfile(filePath))
        graph = create_stage.create_graph_from_usd_files([filePath], as_shape=True)
        self.assertEqual(graph, f"{kGraphName}Shape")

        # check the mayaUsdProxyShape content
        import ufe
        import mayaUsd.ufe

        mayaUsdShapes = cmds.ls(type=kMayaUsdProxyShape, long=True)
        self.assertTrue(mayaUsdShapes)
        proxyShapePath = ufe.PathString.path(mayaUsdShapes[0])
        stage = mayaUsd.ufe.getStage(str(proxyShapePath))
        obj = stage.GetPrimAtPath("/obj")
        self.assertEqual(obj.GetPath(), "/obj")

    def testCreateGraphFromOneFileCommand(self):
        filePath = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "resources", "capsule.usd"
        )
        graph = cmds.bifrostUSDExamples(openStage=True, files=",".join([filePath]))
        self.assertEqual(graph, [f"{kGraphName}Shape"])

    def testCreateGraphFromTwoFilesCommand(self):
        resourcesDir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "resources"
        )

        geoFilePath = os.path.join(resourcesDir, "capsule.usd")
        colorsFilePath = os.path.join(resourcesDir, "capsule_colors.usd")

        graph = cmds.bifrostUSDExamples(
            openStage=True, files=",".join([geoFilePath, colorsFilePath])
        )
        self.assertEqual(graph, [f"{kGraphName}Shape"])

        # check the mayaUsdProxyShape content
        import ufe
        import mayaUsd.ufe

        mayaUsdShapes = cmds.ls(type=kMayaUsdProxyShape, long=True)
        self.assertTrue(mayaUsdShapes)
        proxyShapePath = ufe.PathString.path(mayaUsdShapes[0])

        # share the Bifrost stage with the mayaUsdProxyShape stage to
        # get the same sublayers.
        create_stage._set_shared_stage(graph, True)
        stage = mayaUsd.ufe.getStage(str(proxyShapePath))
        self.assertEqual(
            stage.GetRootLayer().subLayerPaths, [colorsFilePath, geoFilePath]
        )

    def testInsertStageNode(self):
        cmds.bifrostUSDExamples(newStage=True, shape=True)

        self.assertEqual(
            cmds.vnnCompound(f"{kGraphName}Shape", "/", listNodes=True),
            ["output", "create_usd_stage"],
        )

        nodeInfo = author_usd_graph.GraphEditorSelection(
            f"|{kGraphName}|{kGraphName}Shape",
            f"{kGraphName}Shape",
            "/",
            "stage",
            ["create_usd_stage"],
        )

        newNodeDef = {
            "type_name": "BifrostGraph,USD::Stage,save_usd_stage",
            "input": "stage",
            "output": "out_stage",
        }

        author_usd_graph.insert_stage_node(nodeInfo, newNodeDef)

        self.assertEqual(
            cmds.vnnCompound(f"{kGraphName}Shape", "/", listNodes=True),
            ["output", "create_usd_stage", "save_usd_stage"],
        )

        newNodeDef["type_name"] = "BifrostGraph,USD::Stage,add_to_stage"
        author_usd_graph.insert_stage_node(nodeInfo, newNodeDef)

        self.assertEqual(
            cmds.vnnCompound(f"{kGraphName}Shape", "/", listNodes=True),
            ["output", "create_usd_stage", "save_usd_stage", "add_to_stage"],
        )

    def testInsertStageNodeCommand(self):
        cmds.bifrostUSDExamples(newStage=True, shape=True)[0]

        nodeType = "BifrostGraph,USD::Stage,save_usd_stage"
        self.assertEqual(
            cmds.bifrostUSDExamples(
                insertNode=True,
                nodeType=nodeType,
                currentCompound="/",
                nodeSelection="create_usd_stage",
                portSelection="stage",
                inputPort="stage",
                outputPort="out_stage",
            ),
            ["save_usd_stage"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
