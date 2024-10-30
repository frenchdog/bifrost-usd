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

#ifndef USD_STAGE_NODEDEFS_H
#define USD_STAGE_NODEDEFS_H

#include <Bifrost/Object/Object.h>
#include <Amino/Core/Array.h>
#include <Amino/Core/BuiltInTypes.h>
#include <Amino/Core/Ptr.h>
#include <BifrostUsd/Enum.h>
#include <BifrostUsd/Layer.h>
#include <BifrostUsd/Stage.h>

#include "header_parser_macros.h"
#include "nodedef_export.h"

// forward declarations
namespace Amino {
class String;
} // namespace Amino

namespace USD {
namespace Stage {

USD_NODEDEF_DECL
void open_stage_from_layer(const BifrostUsd::Layer&                 root_layer,
                           const Amino::Array<Amino::String>&       mask,
                           const BifrostUsd::InitialLoadSet         load,
                           const int                                layer_index
                               AMINO_ANNOTATE("Amino::Port value=-1"),
                           Amino::MutablePtr<BifrostUsd::Stage>&    stage)
    USDNODE_DOC_ICON("open_stage_from_layer",
                     "USD_Stage_open_stage_from_layer.md",
                     "usd_stage.svg");

USD_NODEDEF_DECL
void open_stage_from_cache(const Amino::long_t              id AMINO_ANNOTATE("Amino::Port metadata=[{UiSoftMin, string, 0}]"),
                           const int                        layer_index
                               AMINO_ANNOTATE("Amino::Port value=-1"),
                           Amino::Ptr<BifrostUsd::Stage>&   stage)
    USDNODE_DOC_ICON("open_stage_from_cache",
                     "USD_Stage_open_stage_from_cache.md",
                     "usd_stage.svg");

USD_NODEDEF_DECL
void set_edit_layer(BifrostUsd::Stage&  stage USDPORT_INOUT("out_stage"),
                    const int            layer_index,
                    const Amino::String& layer_display_name = Amino::String())
    USDNODE_DOC_ICON("set_edit_layer", "USD_Stage_set_edit_layer.md", "make_target.svg");

USD_NODEDEF_DECL
void get_edit_layer(const BifrostUsd::Stage& stage,
                    const bool read_only
                        AMINO_ANNOTATE("Amino::Port value=true"),
                    Amino::Ptr<BifrostUsd::Layer>& edit_layer)
    USDNODE_DOC_ICON("get_edit_layer", "USD_Stage_get_edit_layer.md", "make_target.svg");

USD_NODEDEF_DECL
void set_default_prim(BifrostUsd::Stage&    stage USDPORT_INOUT("out_stage"),
                      const Amino::String&  prim_path)
    USDNODE_INTERNAL("set_default_prim", "USD_Stage_set_default_prim.md");

USD_NODEDEF_DECL
void get_default_prim(const BifrostUsd::Stage&  stage,
                      Amino::String&            prim_path)
    USDNODE_DOC_ICON("get_default_prim", "USD_Stage_get_default_prim.md", "usd_pill.svg");

USD_NODEDEF_DECL
bool set_stage_up_axis(BifrostUsd::Stage&       stage USDPORT_INOUT("out_stage"),
                       const BifrostUsd::UpAxis axis)
    USDNODE_DOC_ICON_X("set_stage_up_axis",
                       "USD_Stage_set_stage_up_axis.md",
                       "usd_stage.svg",
                       "outName=success");

USD_NODEDEF_DECL
void set_stage_time_code(BifrostUsd::Stage& stage USDPORT_INOUT("out_stage"),
                         const float        start,
                         const float        end)
    USDNODE_DOC_ICON("set_stage_time_code", "USD_Stage_set_stage_time_code.md", "usd_stage.svg");

#define SET_STAGE_METADATA(VALUE_TYPE)                                 \
    USD_NODEDEF_DECL                                                   \
    bool set_stage_metadata(                                           \
        BifrostUsd::Stage&      stage USDPORT_INOUT("out_stage"),      \
        const Amino::String&    key,                                   \
        const VALUE_TYPE&       value)                                 \
        USDNODE_INTERNAL_X("set_stage_metadata", "USD_Stage_set_stage_metadata.md", \
                           "outName=success");

SET_STAGE_METADATA(Amino::String)
SET_STAGE_METADATA(Amino::float_t)
SET_STAGE_METADATA(Amino::double_t)
SET_STAGE_METADATA(Amino::int_t)
SET_STAGE_METADATA(Amino::long_t)
SET_STAGE_METADATA(Amino::bool_t)
SET_STAGE_METADATA(Bifrost::Object)


#define GET_STAGE_METADATA(VALUE_TYPE)                                 \
    USD_NODEDEF_DECL                                                   \
    bool get_stage_metadata(                                           \
        const BifrostUsd::Stage&    stage,                             \
        const Amino::String&        key,                               \
        const VALUE_TYPE&           default_and_type,                  \
        VALUE_TYPE&                 value)                             \
        USDNODE_INTERNAL_X("get_stage_metadata", "USD_Stage_get_stage_metadata.md", \
                           "outName=success");

GET_STAGE_METADATA(Amino::String)
GET_STAGE_METADATA(Amino::float_t)
GET_STAGE_METADATA(Amino::double_t)
GET_STAGE_METADATA(Amino::int_t)
GET_STAGE_METADATA(Amino::long_t)
GET_STAGE_METADATA(Amino::bool_t)
GET_STAGE_METADATA(Amino::Ptr<Bifrost::Object>)


USD_NODEDEF_DECL
bool save_stage(const BifrostUsd::Stage&    stage,
                const Amino::String&        file  USDNODE_FILE_BROWSER_SAVE)
    USDNODE_INTERNAL("save_stage", "USD_Stage_save_stage.md");

USD_NODEDEF_DECL
Amino::long_t send_stage_to_cache(const Amino::Ptr<BifrostUsd::Stage>& stage)
    USDNODE_DOC_ICON_X("send_stage_to_cache",
                       "USD_Stage_send_stage_to_cache.md",
                       "usd_stage.svg",
                       "outName=id");

USD_NODEDEF_DECL
void export_stage_to_string(const BifrostUsd::Stage&    stage,
                            Amino::String&              result)
    USDNODE_DOC_ICON("export_stage_to_string",
                     "USD_Stage_export_stage_to_string.md",
                     "usd_default.svg");

USD_NODEDEF_DECL
bool export_stage_to_file(const BifrostUsd::Stage&  stage,
                          const Amino::String&      file  USDNODE_FILE_BROWSER_SAVE)
    USDNODE_DOC_ICON_X("export_stage_to_file",
                       "USD_Stage_export_stage_to_file.md",
                       "write_usd_file.svg",
                       "outName=success");

} // namespace Stage
} // namespace USD

#endif // USD_STAGE_NODEDEFS_H
