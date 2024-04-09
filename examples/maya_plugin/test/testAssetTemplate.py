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
import sys
import unittest

test_dir = os.path.dirname(os.path.realpath(__file__))
maya_usd_model_dir = os.path.join(test_dir, "..", "python")
sys.path.append(maya_usd_model_dir)

from bifrost_usd.component_creator import asset_template  # noqa: E402 // import not at top of file


class AssetTemplateTestCase(unittest.TestCase):
    def testGetGeoInfo(self):
        filePath = "/props/spheres/geo/spheres.usd"
        expectedGeoInfo = {
            "variant": "spheres",
            "purpose": "default",
            "relative_path": "geo/spheres.usd",
        }
        self.assertEqual(asset_template.get_geo_file_info(filePath), expectedGeoInfo)

        filePath = "/props/spheres/geo/spheres_default.usd"
        expectedGeoInfo = {
            "variant": "spheres",
            "purpose": "default",
            "relative_path": "geo/spheres_default.usd",
        }
        self.assertEqual(asset_template.get_geo_file_info(filePath), expectedGeoInfo)

        filePath = "/props/spheres/geo/spheres_proxy.usd"
        expectedGeoInfo = {
            "variant": "spheres",
            "purpose": "proxy",
            "relative_path": "geo/spheres_proxy.usd",
        }
        self.assertEqual(asset_template.get_geo_file_info(filePath), expectedGeoInfo)

        filePath = "/props/spheres/geo/spheres_render.usd"
        expectedGeoInfo = {
            "variant": "spheres",
            "purpose": "render",
            "relative_path": "geo/spheres_render.usd",
        }
        self.assertEqual(asset_template.get_geo_file_info(filePath), expectedGeoInfo)

        filePath = "/props/spheres/geo/spheres_and_cubes.usd"
        expectedGeoInfo = {
            "variant": "spheres_and_cubes",
            "purpose": "default",
            "relative_path": "geo/spheres_and_cubes.usd",
        }
        self.assertEqual(asset_template.get_geo_file_info(filePath), expectedGeoInfo)

        filePath = "/props/spheres/geo/spheres_and_cubes_render.usd"
        expectedGeoInfo = {
            "variant": "spheres_and_cubes",
            "purpose": "render",
            "relative_path": "geo/spheres_and_cubes_render.usd",
        }
        self.assertEqual(asset_template.get_geo_file_info(filePath), expectedGeoInfo)

        filePath = "/props/spheres/geo/render.usd"
        expectedGeoInfo = {
            "variant": "render",
            "purpose": "default",
            "relative_path": "geo/render.usd",
        }
        self.assertEqual(asset_template.get_geo_file_info(filePath), expectedGeoInfo)

        filePath = "/props/spheres/geo/render_render.usd"
        expectedGeoInfo = {
            "variant": "render",
            "purpose": "render",
            "relative_path": "geo/render_render.usd",
        }
        self.assertEqual(asset_template.get_geo_file_info(filePath), expectedGeoInfo)

    def testGetGeoVariants(self):
        geoDir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "resources",
            "components",
            "spheres",
            "geo",
        )

        geoDirData = asset_template.get_geo_dir_data(geoDir)

        self.assertFalse(geoDirData.get("notvalid_extension"))

        spheresVariantGeos = geoDirData.get("spheres")
        self.assertTrue(spheresVariantGeos)
        self.assertEqual(spheresVariantGeos.guide, "geo/spheres_guide.usd")
        self.assertEqual(spheresVariantGeos.proxy, "geo/spheres_proxy.usd")
        self.assertEqual(spheresVariantGeos.default, "geo/spheres.usd")
        self.assertEqual(spheresVariantGeos.render, "geo/spheres_render.usd")

        spheresDamagedVariantGeos = geoDirData.get("spheres_damaged")
        self.assertTrue(spheresDamagedVariantGeos)
        self.assertEqual(
            spheresDamagedVariantGeos.guide, "geo/spheres_damaged_guide.usd"
        )
        self.assertEqual(
            spheresDamagedVariantGeos.proxy, "geo/spheres_damaged_proxy.usd"
        )
        self.assertEqual(spheresDamagedVariantGeos.default, "geo/spheres_damaged.usd")
        self.assertEqual(
            spheresDamagedVariantGeos.render, "geo/spheres_damaged_render.usd"
        )

    def testGetModelNameInfo(self):
        names = asset_template.get_model_name_info("MyAsset")
        self.assertEqual(len(names), 3)
        self.assertEqual(names, ("MyAsset", "default", "default"))

        names = asset_template.get_model_name_info("MyAsset_new_render")
        self.assertEqual(len(names), 3)
        self.assertEqual(names, ("MyAsset", "new", "render"))

        names = asset_template.get_model_name_info("MyAsset_new_and_shinny_render")
        self.assertEqual(len(names), 3)
        self.assertEqual(names, ("MyAsset", "new_and_shinny", "render"))

        names = asset_template.get_model_name_info("MyAsset_clean_edges")
        self.assertEqual(len(names), 3)
        self.assertEqual(names, ("MyAsset", "clean_edges", "default"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
