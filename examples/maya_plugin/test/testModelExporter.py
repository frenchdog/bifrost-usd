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
import tempfile

from maya import cmds
from maya import standalone

from bifrost_usd.component_creator import model_exporter as mex


class ModelExporterTestCase(unittest.TestCase):
    plugins_loaded = False

    @classmethod
    def setUpClass(cls):
        if not cls.plugins_loaded:
            standalone.initialize("bifrost-usd-export-maya-model")
            cmds.loadPlugin("mayaUsdPlugin", quiet=True)
            cmds.loadPlugin("bifrostUSDExamples.py", quiet=True)
            cls.plugins_loaded = True

    @classmethod
    def tearDownClass(cls):
        standalone.uninitialize()

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        cmds.file(f=True, new=True)

    def checkUsdExport(self, exporter):
        from pxr import Usd
        stage = Usd.Stage.Open(exporter.file_path)
        self.assertTrue(stage)

        prim = stage.GetDefaultPrim()
        self.assertTrue(prim)
        self.assertEqual(prim.GetTypeName(), "Xform")
        geoScopePrim = stage.GetPrimAtPath(prim.GetPath().AppendChild("geo"))
        self.assertTrue(geoScopePrim)
        self.assertEqual(geoScopePrim.GetTypeName(), "Scope")
        self.assertTrue(len(geoScopePrim.GetChildren()) > 0)

    def testInvalidSelection(self):
        # Nothing selected
        self.assertFalse(mex.ModelExporter.get_valid_selection())

        # A mesh is not a valid selection
        cmds.polySphere()
        self.assertFalse(mex.ModelExporter.get_valid_selection())

        # A group with a mesh inside is not a valid selection
        cmds.group("pSphere1", name="group_for_the_geo")
        self.assertFalse(mex.ModelExporter.get_valid_selection())

        # A group with a group with a mesh inside is a valid selection
        cmds.group("group_for_the_geo", name="Model")
        self.assertTrue(mex.ModelExporter.get_valid_selection())

        # but it should rename "group_for_the_geo" to "geo"
        self.assertFalse(cmds.ls("group_for_the_geo"))
        self.assertTrue(cmds.ls("geo"))

    def testNoAutomaticNamingExport(self):
        cmds.polySphere()
        cmds.group("pSphere1", name="group_for_the_geo")
        cmds.group("group_for_the_geo", name="Model")

        exporter = mex.ModelExporter(
            self.test_dir,
            model_name="TestModel",
            autoNaming=False,
        )
        self.assertEqual(exporter.model_path, "|Model")
        self.assertEqual(exporter.file_path, os.path.join(self.test_dir, "TestModel", "geo", "default.usd"))
        exporter.do()
        self.checkUsdExport(exporter)

    def testAutomaticNamingExport(self):
        cmds.polySphere()
        cmds.group("pSphere1", name="group_for_the_geo")
        cmds.group("group_for_the_geo", name="Model")

        exporter = mex.ModelExporter(
            self.test_dir,
            model_name="NotUsedModelName",
            autoNaming=True,
        )
        self.assertEqual(exporter.model_path, "|Model")
        self.assertEqual(exporter.file_path,  os.path.join(self.test_dir, "Model", "geo", "default.usd"))
        exporter.do()
        self.checkUsdExport(exporter)

    def testAutomaticNamingVariantAndPurposeExport(self):
        cmds.polySphere()
        cmds.group("pSphere1", name="group_for_the_geo")
        cmds.group("group_for_the_geo", name="model_clean_render")

        exporter = mex.ModelExporter(
            self.test_dir,
            autoNaming=True
        )
        self.assertEqual(exporter.model_path, "|model_clean_render")
        self.assertEqual(exporter.file_path, os.path.join(self.test_dir, "model", "geo", "clean_render.usd"))
        exporter.do()
        self.checkUsdExport(exporter)

    def testNoAutomaticNamingVariantAndPurposeExport(self):
        cmds.polySphere()
        cmds.group("pSphere1", name="group_for_the_geo")
        cmds.group("group_for_the_geo", name="model_dirty_render")

        exporter = mex.ModelExporter(
            self.test_dir,
            model_name="model",
            variant="dirty",
            purpose="render",
            autoNaming=False
        )
        self.assertEqual(exporter.model_path, "|model_dirty_render")
        self.assertEqual(exporter.file_path, os.path.join(self.test_dir, "model", "geo", "dirty_render.usd"))
        exporter.do()
        self.checkUsdExport(exporter)


if __name__ == "__main__":
    unittest.main(verbosity=2)
