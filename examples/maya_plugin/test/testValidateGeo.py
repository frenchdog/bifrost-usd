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

from maya import cmds
from maya import standalone

""" Test checking the validity of a USD file storing geometries.
"""


class ValidateGeoTestCase(unittest.TestCase):
    plugins_loaded = False

    @classmethod
    def setUpClass(cls):
        if not cls.plugins_loaded:
            standalone.initialize("component_creator")
            cmds.loadPlugin("mayaUsdPlugin", quiet=True)
            cmds.loadPlugin("bifrostUSDExamples.py", quiet=True)
            cls.plugins_loaded = True

    @classmethod
    def tearDownClass(cls):
        standalone.uninitialize()

    def testAssetWithoutGeoPrim(self):
        from bifrost_usd.component_creator import component as cpn

        geoFilePath = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "resources",
            "components",
            "asset_without_geo_prim",
            "geo",
            "asset_without_geo_prim.usd",
        )
        self.assertEqual(
            cpn._validate_geo_layer(geoFilePath),
            f"Missing 'geo' prim in geo layer {geoFilePath}",
        )

    def testAssetWithGeoPrim(self):
        from bifrost_usd.component_creator import component as cpn

        geoFilePath = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "resources",
            "components",
            "quad",
            "geo",
            "quad.usda",
        )
        self.assertEqual(
            cpn._validate_geo_layer(geoFilePath), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
