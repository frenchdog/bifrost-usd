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

from maya import cmds
from maya import standalone

""" Test only the authoring of compounds in the "componentCreator" graph. No stage output is created.
"""


class ComponentCreatorGraphOnlyTestCase(unittest.TestCase):
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
        cmds.file(f=True, new=True)

    def testFindConnectedModelVariantCompounds(self):
        from bifrost_usd.component_creator import component as cpn

        from bifrost_usd.graph_api import GraphAPI
        from bifrost_usd.component_creator.component import find_bifrost_component_graph
        graphAPI = GraphAPI(find_bifrost_component_graph)

        graph = cpn._create_empty_graph()
        # use the graph name to find it in the Maya scene
        self.assertEqual(graph, cpn.kGraphName)

        cpn._create_component_compound(graph)
        self.assertEqual(
            graphAPI.find_nodes(cpn.kCreateComponentCompound), ["create_usd_component"]
        )
        # it should not create any new "create_usd_component" compound
        cpn._create_component_compound(graph)
        self.assertEqual(
            graphAPI.find_nodes(cpn.kCreateComponentCompound), ["create_usd_component"]
        )

        self.assertEqual(graphAPI.find_nodes(cpn.kModelVariantCompound), [])
        cpn._create_model_variant_compound(graph, variant_name="Model_A", connect=True)
        self.assertEqual(cpn.get_model_variant_nodes(), ["define_usd_model_variant"])

        # we create an unconnected node. It should not be part of the model variant nodes used
        # by the graph.
        cpn._create_model_variant_compound(graph, variant_name="Model_B", connect=False)
        # the node is created
        self.assertEqual(
            graphAPI.find_nodes(cpn.kModelVariantCompound),
            ["define_usd_model_variant", "define_usd_model_variant1"],
        )
        # but is not part of the "create_usd_component" graph
        self.assertEqual(cpn.get_model_variant_nodes(), ["define_usd_model_variant"])

        # now create a second model variant compound but connected to the "create_usd_component"
        cpn._create_model_variant_compound(graph, variant_name="Model_B", connect=True)
        self.assertEqual(
            cpn.get_model_variant_nodes(),
            ["define_usd_model_variant", "define_usd_model_variant2"],
        )

    def testFindConnectedLookVariantCompounds(self):
        from bifrost_usd.component_creator import component as cpn

        from bifrost_usd.graph_api import GraphAPI
        from bifrost_usd.component_creator.component import find_bifrost_component_graph
        graphAPI = GraphAPI(find_bifrost_component_graph)

        # initialize component graph
        graph = cpn._create_empty_graph()
        cpn._create_component_compound(graph)

        # add two "define_usd_model_variant" compounds
        cpn._create_model_variant_compound(graph, variant_name="Model_A")
        cpn._create_model_variant_compound(graph, variant_name="Model_B")

        cpn.set_default_model_variant("Model_A")
        cpn.add_look("My Default Look")
        self.assertEqual(cpn.default_model_variant(), "Model_A")
        self.assertEqual(cpn.default_look_variant(), "My_Default_Look")

        self.assertEqual(
            cpn.get_look_variant_nodes(model_variant="Model_A"),
            ["define_usd_look_variant"],
        )
        self.assertEqual(cpn.get_look_variant_nodes(model_variant="Model_B"), [])

        # add a "define_usd_material_binding" compound
        bindNode = cpn._add_bind_node()
        self.assertEqual(bindNode, "define_usd_material_binding")

        self.assertEqual(
            cmds.vnnNode(cpn.kGraphName, f"/{bindNode}", listPorts=1, connected=True),
            ["define_usd_material_binding.material_binding"],
        )

        self.assertEqual(cpn.current_binding_nodes(), ["define_usd_material_binding"])

        self.assertEqual(
            graphAPI.port_children("define_usd_look_variant", "material_bindings"),
            ["material_binding"],
        )
        graphAPI.disconnect(
            "define_usd_material_binding.material_binding",
            "define_usd_look_variant.material_bindings.material_binding",
        )
        self.assertEqual(cpn.current_binding_nodes(), [])

        graphAPI.connect_to_fanin_port(
            from_node="define_usd_material_binding",
            to_node="define_usd_look_variant",
            parent_port="material_bindings",
            from_port="material_binding",
        )
        self.assertEqual(cpn.current_binding_nodes(), ["define_usd_material_binding"])

        # add a path expression node storing a relative geo path
        pathExprNode1 = cpn._get_or_create_pathexpr_node("geometry1")
        self.assertEqual(pathExprNode1, "path_expression")
        self.assertEqual(graphAPI.param(pathExprNode1, "prim_path"), "geometry1")

        # connect to the bind node
        newChildPort = graphAPI.get_new_fanin_name(bindNode, "prim_paths", "output")
        self.assertEqual(newChildPort, "output")
        graphAPI.connect_to_fanin_port(pathExprNode1, bindNode, "prim_paths", "output")
        childPortNames = cmds.vnnNode(
            cpn.kGraphName, f"/{bindNode}", listPortChildren="prim_paths"
        )
        self.assertEqual(childPortNames, ["output"])

        # connect a second path expression node to the bind node
        newChildPort = graphAPI.get_new_fanin_name(bindNode, "prim_paths", "output")
        self.assertEqual(newChildPort, "output1")

        valueNode2 = cpn._get_or_create_pathexpr_node("geometry2")
        graphAPI.connect_to_fanin_port(valueNode2, bindNode, "prim_paths", "output")

        childPortNames = cmds.vnnNode(
            cpn.kGraphName, f"/{bindNode}", listPortChildren="prim_paths"
        )
        self.assertEqual(childPortNames, ["output", "output1"])

        # disconnect "geometry1" from the binding node
        inputPort = bindNode + "." + "prim_paths" + "." + "output"
        graphAPI.disconnect(f"{pathExprNode1}.output", f"{inputPort}")

        childPortNames = cmds.vnnNode(
            cpn.kGraphName, f"/{bindNode}", listPortChildren="prim_paths"
        )
        self.assertEqual(childPortNames, ["output1"])

        # reconnect first value node
        newChildPort = graphAPI.get_new_fanin_name(bindNode, "prim_paths", "output")
        self.assertEqual(newChildPort, "output2")

        graphAPI.connect_to_fanin_port(pathExprNode1, bindNode, "prim_paths", "output")
        childPortNames = cmds.vnnNode(
            cpn.kGraphName, f"/{bindNode}", listPortChildren="prim_paths"
        )
        self.assertEqual(childPortNames, ["output1", "output2"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
