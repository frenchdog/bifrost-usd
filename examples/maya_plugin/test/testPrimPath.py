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
from maya import standalone

from bifrost_usd.author_usd_graph import to_prim_path
from bifrost_usd.author_usd_graph import is_new_path_a_parent
from unittest.mock import patch


class PrimPathTestCase(unittest.TestCase):
    plugins_loaded = False

    @classmethod
    def setUpClass(cls):
        if not cls.plugins_loaded:
            standalone.initialize("bifrost-usd-prim-path")
            cls.plugins_loaded = True

    def testInvalidPath(self):
        ufePath = ""
        self.assertEqual(to_prim_path(ufePath), "")

        ufePath = "A|B|C"
        self.assertEqual(to_prim_path(ufePath), "")

        ufePath = "|A|B|C"
        self.assertEqual(to_prim_path(ufePath), "")

        ufePath = "|world"
        self.assertEqual(to_prim_path(ufePath), "")

        ufePath = "|world|"
        self.assertEqual(to_prim_path(ufePath), "")

        ufePath = "/world/A/B"
        self.assertEqual(to_prim_path(ufePath), "")

        ufePath = "/A/B"
        self.assertEqual(to_prim_path(ufePath), "")

    def testTransformPrimPath(self):
        ufePath = "|world|A|B|C"
        self.assertEqual(to_prim_path(ufePath), "/A/B/C")

    @patch("maya.cmds.ls")
    def testMeshPrimPath(self, mock_cmds):
        ufePath = "|world|A|B|C|CShape"
        self.assertEqual(to_prim_path(ufePath), "/A/B/C")

    def test_isNewPathAParent(self):
        path = "/A/X/Y"
        new_path = "/Y"
        self.assertTrue(is_new_path_a_parent(path, new_path))
        new_path = "/B/Y"
        self.assertTrue(is_new_path_a_parent(path, new_path))

    # we don't support reparenting non leaf nodes
    def DISABLED_test_isNewPathAParent(self):
        path = "/Model/geo/pCube1"
        new_path = "/Model/NEW_GROUP/geo"
        self.assertTrue(is_new_path_a_parent(path, new_path))


if __name__ == "__main__":
    unittest.main(verbosity=2)
