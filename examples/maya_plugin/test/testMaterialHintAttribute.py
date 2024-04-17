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

from bifrost_usd.component_creator.material_hint_attribute import apply_to_selection
from bifrost_usd.component_creator import model_exporter as mex


class MaterialHintAttributeTestCase(unittest.TestCase):
    plugins_loaded = False

    @classmethod
    def setUpClass(cls):
        if not cls.plugins_loaded:
            standalone.initialize("material-hint-attribute")
            cmds.loadPlugin("mayaUsdPlugin", quiet=True)
            cls.plugins_loaded = True

    @classmethod
    def tearDownClass(cls):
        standalone.uninitialize()

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        cmds.file(f=True, new=True)

    def testApplyToSelection(self):
        # In Maya
        cmds.polySphere()
        cmds.group("pSphere1", name="geo")
        cmds.group("geo", name="Ball")

        apply_to_selection("plastic")
        self.assertEqual(cmds.getAttr("Ball.BIF_material_hint"), "plastic")

        # Export to USD
        exporter = mex.ModelExporter(
            self.test_dir,
            autoNaming=False,
        )
        self.assertEqual(
            exporter.file_path,
            os.path.join(self.test_dir, "Ball", "geo", "default.usd"),
        )
        exporter.do()

        from pxr import Usd, Sdf

        stage = Usd.Stage.Open(exporter.file_path)
        self.assertTrue(stage)
        prim = stage.GetDefaultPrim()
        self.assertTrue(prim)
        self.assertEqual(prim.GetPath(), Sdf.Path("/Ball"))
        self.assertTrue(
            materialHintAttrib := prim.GetAttribute("primvars:bifrost:material_hint")
        )
        self.assertEqual(materialHintAttrib.Get(), "plastic")


if __name__ == "__main__":
    unittest.main(verbosity=2)
