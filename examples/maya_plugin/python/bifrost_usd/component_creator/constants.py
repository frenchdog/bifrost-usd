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
from typing import Final

kArnoldMeshPrimvarsCompound: Final = (
    "BifrostGraph,USD::Arnold,define_arnold_usd_mesh_primvars"
)
kComponentStageName: Final = "componentCreatorStage"
kComponentStageShape: Final = f"{kComponentStageName}Shape"
kComponentStageShapeFullName: Final = f"|{kComponentStageName}|{kComponentStageShape}"
kComponentStageUfePath: Final = f"|world{kComponentStageShapeFullName}"
kCreateComponentCompound: Final = "BifrostGraph,USD::Model,create_usd_component"
kDefaultMatLibFileName: Final = "material_library.usd"
kGraphName: Final = "componentCreator"
kHUD_UsdComponentVariants: Final = "HUD_UsdComponentVariants"
kLookVariantCompound: Final = "BifrostGraph,USD::Model,define_usd_look_variant"
kMaterialBindingCompound: Final = "BifrostGraph,USD::Model,define_usd_material_binding"
kMatLibName: Final = "componentMaterialLibrary"
kMatLibShapeFullName: Final = f"|{kMatLibName}|{kMatLibName}Shape"
kMatLibUfePath: Final = f"|world{kMatLibShapeFullName}"
kModelVariantCompound: Final = "BifrostGraph,USD::Model,define_usd_model_variant"
kPathExpressionCompound: Final = "BifrostGraph,USDLab::PatternMatching,path_expression"
