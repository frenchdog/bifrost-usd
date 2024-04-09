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

""" Test various assign/unassign workflows.
"""


def _create_quad_component(cpn, testDir, save=False):
    model_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "resources",
        "components",
        "quad",
    )
    testModelDir = os.path.join(testDir, "quad")
    copy_tree(model_dir, testModelDir)
    cmds.file(f=True, new=True)
    cpn.component_creator(testModelDir, version="")

    if save:
        cpn.save()


def _get_stage(cpn):
    """Run the Bifrost graph and get the generated stage"""
    from pxr import Usd, UsdUtils

    cacheIdValue = cpn.run_graph()
    cacheId = Usd.StageCache.Id.FromLongInt(cacheIdValue)

    StageCache = UsdUtils.StageCache.Get()
    stage = StageCache.Find(cacheId)
    return stage


def _check_binding(testCase, prim, material_path):
    from pxr import Sdf, UsdShade

    bindingAPI = UsdShade.MaterialBindingAPI.Apply(prim)
    rel = bindingAPI.GetDirectBindingRel()
    testCase.assertTrue(rel)
    testCase.assertEqual(rel.GetTargets(), [Sdf.Path(material_path)])


class ComponentCreatorMaterialBindingTestCase(unittest.TestCase):
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
        # pass

    def testSaveComponentWithoutMaterials(self):
        from bifrost_usd.component_creator import component as cpn
        from pxr import Usd

        _create_quad_component(cpn, self.testDir)

        # check there is no quad.usd on disk
        quadPath = os.path.join(cpn.get_model_dir(), f"{cpn.name()}.usd")
        self.assertFalse(os.path.isfile(quadPath))

        # Enable save component to disk
        cpn.save()

        self.assertTrue(os.path.isfile(quadPath))

        stage = Usd.Stage.Open(quadPath)
        self.assertTrue(stage)

        prim = stage.GetDefaultPrim()
        self.assertTrue(prim)

        self.assertEqual(prim.GetAppliedSchemas(), ["GeomModelAPI"])

    def testAddMaterial(self):
        from bifrost_usd.component_creator import component as cpn
        from bifrost_usd.component_creator.constants import kMatLibUfePath

        _create_quad_component(cpn, self.testDir, save=True)

        # check if the ufePath of new material is from the componentMaterialLibraryShape
        ufeMatPath = cpn.add_new_material()
        self.assertEqual(ufeMatPath, f"{kMatLibUfePath},/mtl/Material1")

        # check if there is the material under mtl scope in the componentCreatorStageShape
        cpn.run_graph()

        matPrim = _get_stage(cpn).GetPrimAtPath("/quad/mtl/Material1")
        self.assertTrue(matPrim)

    def testAssignNewMaterial(self):
        from bifrost_usd.component_creator import component as cpn
        from bifrost_usd.component_creator import constants

        _create_quad_component(cpn, self.testDir, save=True)

        ufeMeshPath = f"{constants.kComponentStageUfePath},/quad/geo/mesh"
        matName = cpn.assign_material(ufeMeshPath)
        self.assertEqual(matName, "Material1")

        # check if there is binding to Material1 on the mesh
        stage = _get_stage(cpn)
        meshPrim = stage.GetPrimAtPath("/quad/geo/mesh")
        self.assertTrue(meshPrim)
        _check_binding(self, meshPrim, "/quad/mtl/Material1")

    def testAssignExistingMaterials(self):
        from bifrost_usd.component_creator import component as cpn
        from bifrost_usd.component_creator import constants

        _create_quad_component(cpn, self.testDir)
        # create Material1, Material2 and Material3
        cpn.add_new_material()
        cpn.add_new_material()
        cpn.add_new_material()

        # assign Material1
        ufeMeshPath = f"{constants.kComponentStageUfePath},/quad/geo/mesh"
        matName = cpn.assign_material(ufeMeshPath, "Material1")
        self.assertEqual(matName, "Material1")

        # check if there is binding to Material1 on the mesh
        stage = _get_stage(cpn)
        meshPrim = stage.GetPrimAtPath("/quad/geo/mesh")
        self.assertTrue(meshPrim)
        _check_binding(self, meshPrim, "/quad/mtl/Material1")

        # unassign Material1
        cpn.unassign_material(ufeMeshPath)
        stage = _get_stage(cpn)
        meshPrim = stage.GetPrimAtPath("/quad/geo/mesh")
        # check there is no more "MaterialBindingAPI" schema applied to the prim
        self.assertEqual(meshPrim.GetAppliedSchemas(), [])

        # assign Material2
        matName = cpn.assign_material(ufeMeshPath, "Material2")
        self.assertEqual(matName, "Material2")

        # check if there is binding to Material2 on the mesh
        stage = _get_stage(cpn)
        meshPrim = stage.GetPrimAtPath("/quad/geo/mesh")
        self.assertTrue(meshPrim)
        _check_binding(self, meshPrim, "/quad/mtl/Material2")

        # assign Material3 on a prim already assigned
        matName = cpn.assign_material(ufeMeshPath, "Material3")
        self.assertEqual(matName, "Material3")

        # check if there is binding to Material3 on the mesh
        stage = _get_stage(cpn)
        meshPrim = stage.GetPrimAtPath("/quad/geo/mesh")
        self.assertTrue(meshPrim)
        _check_binding(self, meshPrim, "/quad/mtl/Material3")

    def testAssignInNewLook(self):
        from bifrost_usd.component_creator import component as cpn
        from bifrost_usd.component_creator import constants

        _create_quad_component(cpn, self.testDir)
        # assign Material1 in default look
        ufeMeshPath = f"{constants.kComponentStageUfePath},/quad/geo/mesh"
        matName = cpn.assign_material(ufeMeshPath)
        self.assertEqual(matName, "Material1")

        # check if there is binding to Material1 on the mesh
        stage = _get_stage(cpn)
        meshPrim = stage.GetPrimAtPath("/quad/geo/mesh")
        self.assertTrue(meshPrim)
        _check_binding(self, meshPrim, "/quad/mtl/Material1")

        # create a new look and assign the material in it
        cpn.add_look("NewLook")
        ufeMeshPath = f"{constants.kComponentStageUfePath},/quad/default/quad/geo/mesh"
        # assign a new material
        matName = cpn.assign_material(ufeMeshPath)
        self.assertEqual(matName, "Material2")

        # check if there is binding to Material1 on the mesh
        stage = _get_stage(cpn)
        meshPrim = stage.GetPrimAtPath("/quad/default/quad/geo/mesh")
        self.assertTrue(meshPrim)
        _check_binding(self, meshPrim, "/quad/default/quad/mtl/Material2")

        # now go back to default look
        cpn.set_default_look_variant("default")
        # and check if there is still the binding to Material1 on the mesh
        stage = _get_stage(cpn)
        meshPrim = stage.GetPrimAtPath("/quad/default/quad/geo/mesh")
        self.assertTrue(meshPrim)
        _check_binding(self, meshPrim, "/quad/default/quad/mtl/Material1")


if __name__ == "__main__":
    unittest.main(verbosity=1)
