//-
// Copyright 2024 Autodesk, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//+

#ifndef USD_GEOM_NODEDEFS_H
#define USD_GEOM_NODEDEFS_H

#include <Amino/Core/Array.h>
#include <Amino/Core/Ptr.h>
#include <Bifrost/Math/Types.h>
#include <BifrostUsd/Prim.h>
#include <BifrostUsd/Stage.h>

#include "header_parser_macros.h"
#include "nodedef_export.h"

// forward declarations
namespace Amino {
class String;
} // namespace Amino

namespace USD {

namespace Prim {

USD_NODEDEF_DECL
bool get_usd_geom_xform_vectors(
    const BifrostUsd::Prim& prim,
    const float frame
        AMINO_ANNOTATE("Amino::Port value=1 metadata=[{quick_create, "
                      "string, Core::Time::time.frame}] "),
    Bifrost::Math::float3&         translation,
    Bifrost::Math::float3&         rotation,
    Bifrost::Math::float3&         scale,
    Bifrost::Math::float3&         pivot,
    Bifrost::Math::rotation_order& rotation_order)
    USDNODE_DOC_ICON_X("get_usd_geom_xform_vectors",
                       "USD_Prim_get_usd_geom_xform_vectors.md",
                       "usd_default.svg",
                       "outName=success");

USD_NODEDEF_DECL
bool compute_usdgeom_extent(
    const BifrostUsd::Prim& prim,
    const float frame
        AMINO_ANNOTATE("Amino::Port value=1 metadata=[{quick_create, "
                      "string, Core::Time::time.frame}] "),
    const bool local AMINO_ANNOTATE("Amino::Port value=true"),
    Amino::MutablePtr<Amino::Array<Bifrost::Math::float3>>& extent)
    USDNODE_DOC_ICON_X("compute_usdgeom_extent",
                       "USD_Prim_compute_usdgeom_extent.md",
                       "usd_default.svg",
                       "outName=success");

USD_NODEDEF_DECL
bool usd_point_instancer(
    BifrostUsd::Stage& stage                 USDPORT_INOUT("out_stage"),
    const Amino::String&                       prim_path,
    const Amino::Array<Amino::String>&         prototypes,
    const Amino::Array<int>&                   protoindices,
    const Amino::Array<Bifrost::Math::float3>& positions,
    const Amino::Array<Bifrost::Math::float4>& orientations,
    const Amino::Array<Bifrost::Math::float3>& scales,
    const Amino::Array<Bifrost::Math::float3>& velocities,
    const Amino::Array<Bifrost::Math::float3>& accelerations,
    const Amino::Array<Bifrost::Math::float3>& angular_velocities,
    const Amino::Array<Amino::long_t>&             invisible_ids)
    USDNODE_DOC_ICON_X("usd_point_instancer",
                       "USD_Prim_usd_point_instancer.md",
                       "point_instancer.svg",
                       "outName=success");

USD_NODEDEF_DECL
bool usd_volume(BifrostUsd::Stage& stage USDPORT_INOUT("out_stage"),
                const Amino::String&       prim_path,
                const BifrostUsd::VolumeFieldFormat file_format,
                const Amino::Array<Amino::String>&    field_names,
                const Amino::Array<Amino::String>&    file_paths,
                const Amino::Array<Amino::String>&    relationship_names,
                const float frame                     AMINO_ANNOTATE(
                    "Amino::Port value=1 metadata=[{quick_create, "
                    "string, Core::Time::time.frame}] "))
    USDNODE_DOC_ICON("usd_volume", "USD_Prim_usd_volume.md", "usd_default.svg");

USD_NODEDEF_DECL
bool translate_prim(BifrostUsd::Stage& stage    USDPORT_INOUT("out_stage"),
                    const Amino::String&          prim_path,
                    const Bifrost::Math::double3& translation,
                    const bool                    enable_time,
                    const float                   frame) //
    USDNODE_DOC_ICON_X("translate_prim",
                       "USD_Prim_translate_prim.md",
                       "move.svg",
                       "outName=success");

USD_NODEDEF_DECL
bool rotate_prim(BifrostUsd::Stage& stage USDPORT_INOUT("out_stage"),
                 const Amino::String&       prim_path,
                 const Bifrost::Math::rotation_order& rotation_order,
                 const Bifrost::Math::float3&         rotation AMINO_ANNOTATE("Amino::Port metadata=[{UiSoftMin, string, -180}, {UiSoftMax, string, 180}]"),
                 const bool                           enable_time,
                 const float                          frame) //
    USDNODE_DOC_ICON_X("rotate_prim",
                       "USD_Prim_rotate_prim.md",
                       "rotate.svg",
                       "outName=success");

USD_NODEDEF_DECL
bool scale_prim(BifrostUsd::Stage& stage USDPORT_INOUT("out_stage"),
                const Amino::String&       prim_path,
                const Bifrost::Math::float3& scale
                    AMINO_ANNOTATE("Amino::Port value={x:1.0f, y:1.0f, z:1.0f}"),
                const bool  enable_time,
                const float frame) //
    USDNODE_DOC_ICON_X("scale_prim",
                       "USD_Prim_scale_prim.md",
                       "scale.svg",
                       "outName=success");

USD_NODEDEF_DECL
bool set_prim_pivot(BifrostUsd::Stage& stage   USDPORT_INOUT("out_stage"),
                    const Amino::String&         prim_path,
                    const Bifrost::Math::float3& pivot) //
    USDNODE_DOC_ICON_X("set_prim_pivot",
                       "USD_Prim_set_prim_pivot.md",
                       "usd_default.svg",
                       "outName=success");

USD_NODEDEF_DECL
bool get_usd_geom_points(
    const BifrostUsd::Prim& prim,
    const bool                local_space,
    const float frame
        AMINO_ANNOTATE("Amino::Port value=1 metadata=[{quick_create, "
                      "string, Core::Time::time.frame}] "),
    Amino::MutablePtr<Amino::Array<Bifrost::Math::float3>>& points)
    USDNODE_DOC_ICON_X("get_usd_geom_points",
                       "USD_Prim_get_usd_geom_points.md",
                       "usd_default.svg",
                       "outName=success");

} // namespace Prim
} // namespace USD

#endif // USD_GEOM_NODEDEFS_H
