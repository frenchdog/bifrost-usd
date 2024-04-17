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
import unittest

import os

import shutil
import tempfile
from distutils.dir_util import copy_tree

from maya import cmds
from maya import standalone

""" Test only the authoring of compounds in the "componentCreator" graph,
 including stage output and material library connection.
"""


class ComponentCreatorTestCase(unittest.TestCase):
    plugins_loaded = False

    @classmethod
    def setUpClass(cls):
        if not cls.plugins_loaded:
            standalone.initialize("component_creator")
            cmds.loadPlugin("mayaUsdPlugin", quiet=True)
            cmds.loadPlugin("bifrostGraph", quiet=True)
            cmds.loadPlugin("bifrostUSDExamples.py", quiet=True)
            cls.plugins_loaded = True

    @classmethod
    def tearDownClass(cls):
        standalone.uninitialize()

    def setUp(self):
        # Create a temporary directory
        self.testDir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.testDir)

    def _copy_asset(self, name, version=""):
        model_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "resources",
            "components",
            name,
        )
        testModelDir = os.path.join(self.testDir, name)
        copy_tree(model_dir, testModelDir)
        return testModelDir

    def testCreateBifrostGraph(self):
        from bifrost_usd.component_creator import component as cpn
        from bifrost_usd.component_creator import purpose

        from bifrost_usd.component_creator.component import find_bifrost_component_graph
        from bifrost_usd.graph_api import bifrost_version, GraphAPI

        graphAPI = GraphAPI(find_bifrost_component_graph)

        modelName = "spheres"
        version = "1"
        modelDir = self._copy_asset(modelName, version)

        cmds.file(f=True, new=True)
        cpn.component_creator(modelDir, version=version)

        """ No looks or materials added in this section """
        # check parameter values on "create_usd_component" compound
        self.assertEqual(cpn.name(), modelName)
        self.assertEqual(cpn.model_version(), version)
        self.assertEqual(cpn.search_mode(), "Custom")
        self.assertEqual(
            cpn.sub_directory(), os.path.normpath(os.path.join(modelDir, ".."))
        )
        self.assertEqual(cpn.geometry_scope_name(), "geo")
        self.assertEqual(cpn.model_variant_set_name(), "Model")
        self.assertEqual(cpn.default_model_variant(), "spheres")
        self.assertEqual(cpn.default_look_variant(), "")
        self.assertEqual(cpn.material_scope_name(), "mtl")
        self.assertEqual(cpn.look_variant_set_name(), "Look")
        self.assertEqual(cpn.material_library_file(), "")

        self.assertEqual(cpn.get_model_variant_names(), ["spheres", "spheres_damaged"])

        # switch to render purpose
        purpose.showRenderPurposes()
        self.assertFalse(cmds.getAttr(f"{cpn.kComponentStageShape}.drawGuidePurpose"))
        self.assertFalse(cmds.getAttr(f"{cpn.kComponentStageShape}.drawProxyPurpose"))
        self.assertTrue(cmds.getAttr(f"{cpn.kComponentStageShape}.drawRenderPurpose"))

        ########################################################################

        """ Starting authoring the graph to add looks, bindings, etc """

        # add first look
        self.assertEqual(cpn.get_look_variant_nodes(), [])
        self.assertFalse(
            "define_usd_look_variant"
            in graphAPI.find_nodes("BifrostGraph,USD::Model,define_usd_look_variant")
        )
        cpn.add_look("first_look")
        self.assertEqual(cpn.default_look_variant(), "first_look")
        self.assertTrue(
            "define_usd_look_variant"
            in graphAPI.find_nodes("BifrostGraph,USD::Model,define_usd_look_variant")
        )

        self.assertEqual(cpn.get_look_variant_nodes(), ["define_usd_look_variant"])
        self.assertEqual(
            cpn.get_look_variant_nodes(model_variant="spheres"),
            ["define_usd_look_variant"],
        )
        self.assertEqual(
            cpn.get_look_variant_nodes(model_variant="spheres_damaged"), []
        )

        self.assertEqual(
            graphAPI.param("define_usd_look_variant", "variant_name"),
            "first_look",
        )

        # add material library
        self.assertEqual(cpn.material_library_file(), "")
        self.assertFalse(cmds.ls(cpn.kMatLibShapeFullName))
        cpn.create_material_library()
        self.assertTrue(cmds.ls(cpn.kMatLibShapeFullName))

        self.assertEqual(
            cpn.material_library_file(),
            os.path.join(modelDir, version, "mtl", cpn.kDefaultMatLibFileName),
        )

        self.assertFalse("define_usd_material_binding" in graphAPI.find_nodes())
        self.assertFalse("value" in graphAPI.find_nodes())

        sphere1Path = (
            f"{cpn.kComponentStageShapeFullName},/spheres/render/spheres/geo/sphere1"
        )
        # assign an non-existing material to sphere1
        cpn.assign_material(sphere1Path, "IDONTEXIST")
        self.assertFalse(cpn.material_is_in_libary("IDONTEXIST"))
        self.assertFalse(
            graphAPI.find_nodes("BifrostGraph,USD::Model,define_usd_material_binding")
        )

        # assign a new material to sphere1
        cpn.assign_material(sphere1Path)
        self.assertTrue("define_usd_material_binding" in graphAPI.find_nodes())
        self.assertTrue("path_expression" in graphAPI.find_nodes())
        self.assertEqual(
            graphAPI.param("define_usd_material_binding", "material"), "Material1"
        )

        expectedInputPort = "define_usd_material_binding.prim_paths.output"

        # BIFROST-9048:
        # missing parent port name with fan-in connection (fixed after Bifrost 2.8.0.0).
        if bifrost_version().startswith("2.8.0.0"):
            expectedInputPort = "define_usd_material_binding.output"

        self.assertEqual(
            cmds.vnnNode(
                cpn.kGraphName, "/path_expression", connectedTo="output", listConnectedNodes=1
            ),
            [expectedInputPort],
        )
        self.assertEqual(graphAPI.param("path_expression", "prim_path"), "sphere1")

        self.assertEqual(cpn.get_binding_nodes(), ["define_usd_material_binding"])

        # add second look variant on second model variant
        cpn.set_default_model_variant("spheres_damaged")
        cpn.add_look("damaged")
        self.assertEqual(cpn.default_look_variant(), "damaged")
        self.assertTrue("define_usd_look_variant1" in graphAPI.find_nodes())
        self.assertEqual(
            cpn.get_look_variant_nodes(),
            [
                "define_usd_look_variant",
                "define_usd_look_variant1",
                "define_usd_look_variant2",
            ],
        )
        self.assertEqual(
            cpn.get_look_variant_nodes(model_variant="spheres"),
            ["define_usd_look_variant"],
        )
        self.assertEqual(
            cpn.get_look_variant_nodes(model_variant="spheres_damaged"),
            ["define_usd_look_variant1", "define_usd_look_variant2"],
        )

        self.assertEqual(
            graphAPI.param("define_usd_look_variant1", "variant_name"),
            "first_look",
        )

        self.assertEqual(
            graphAPI.param("define_usd_look_variant2", "variant_name"),
            "damaged",
        )

        # assign a new material to sphere2
        sphere2Path = (
            f"{cpn.kComponentStageShapeFullName},/spheres/render/spheres/geo/sphere2"
        )
        cpn.assign_material(sphere2Path)
        self.assertTrue("define_usd_material_binding1" in graphAPI.find_nodes())
        self.assertTrue("path_expression1" in graphAPI.find_nodes())
        self.assertEqual(
            graphAPI.param("define_usd_material_binding1", "material"), "Material2"
        )

        expectedInputPort = "define_usd_material_binding1.prim_paths.output"
        # BIFROST-9048:
        # missing parent port name with fan-in connection (fixed after Bifrost 2.8.0.0).
        if bifrost_version().startswith("2.8.0.0"):
            expectedInputPort = "define_usd_material_binding1.output"

        self.assertEqual(
            cmds.vnnNode(
                cpn.kGraphName, "/path_expression1", connectedTo="output", listConnectedNodes=1
            ),
            [expectedInputPort],
        )
        self.assertEqual(graphAPI.param("path_expression1", "prim_path"), "sphere2")

        self.assertEqual(
            cpn.get_binding_nodes(),
            ["define_usd_material_binding", "define_usd_material_binding1"],
        )

        self.assertEqual(
            cpn.get_binding_nodes(("spheres_damaged", "damaged")),
            ["define_usd_material_binding1"],
        )

        self.assertEqual(
            cpn.get_binding_nodes(("spheres", "first_look")),
            ["define_usd_material_binding"],
        )

        # assign sphere2 a second time to same material should not change number of path expression nodes
        # and binding nodes
        self.assertEqual(graphAPI.find_nodes(cpn.kPathExpressionCompound), ["path_expression", "path_expression1"])
        cpn.assign_material(sphere2Path, "Material2")
        self.assertEqual(
            cpn.get_binding_nodes(("spheres", "first_look")),
            ["define_usd_material_binding"],
        )
        self.assertEqual(
            cpn.get_binding_nodes(("spheres_damaged", "damaged")),
            ["define_usd_material_binding1"],
        )

        self.assertEqual(graphAPI.find_nodes(cpn.kPathExpressionCompound), ["path_expression", "path_expression1"])

        # Now disconnect value1 ...

        expectedInputPort = "define_usd_material_binding1.prim_paths.output"
        # BIFROST-9048:
        # missing parent port name with fan-in connection (fixed after Bifrost 2.8.0.0).
        if bifrost_version().startswith("2.8.0.0"):
            expectedInputPort = "define_usd_material_binding1.output"

        self.assertEqual(graphAPI.connexions("path_expression1", "output"), [expectedInputPort])

        cmds.vnnConnect(
            cpn.kGraphName,
            "/path_expression1.output",
            "/define_usd_material_binding1.prim_paths.output",
            disconnect=True,
        )
        self.assertEqual(graphAPI.connexions("path_expression1", "output"), [])

        # ... and re-assign the same material to the same prim.
        # It should re-use exisiting nodes intead of creating new ones.
        cpn.assign_material(sphere2Path, "Material2")
        self.assertEqual(
            cpn.get_binding_nodes(("spheres_damaged", "damaged")),
            ["define_usd_material_binding1"],
        )
        self.assertEqual(graphAPI.find_nodes(cpn.kPathExpressionCompound), ["path_expression", "path_expression1"])

        # create a new material ...
        cpn.add_new_material()
        self.assertFalse("define_usd_material_binding2" in graphAPI.find_nodes())

        # ... and re-assign sphere2 to this new material
        # it should not create a new binding node but instead reuse existing
        # one with an updated "material" value
        cpn.assign_material(sphere2Path, "Material3")
        self.assertFalse("define_usd_material_binding2" in graphAPI.find_nodes())

        self.assertEqual(
            graphAPI.param("define_usd_material_binding1", "material"), "Material3"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
