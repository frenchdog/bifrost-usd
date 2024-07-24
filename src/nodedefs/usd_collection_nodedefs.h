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

#ifndef USD_COLLECTION_NODEDEFS_H
#define USD_COLLECTION_NODEDEFS_H

// #include <Amino/Core/Array.h>

#include <BifrostUsd/Prim.h>
#include <BifrostUsd/Stage.h>

#include "header_parser_macros.h"
#include "nodedef_export.h"

// forward declarations
namespace Amino {
class String;
} // namespace Amino

namespace USD {

namespace Collection {

USD_NODEDEF_DECL
bool get_or_create_collection(BifrostUsd::Stage& stage
                                                   USDPORT_INOUT("out_stage"),
                              const Amino::String& prim_path,
                              const Amino::String& collection_name,
                              const BifrostUsd::ExpansionRule    rule,
                              const Amino::Array<Amino::String>& include_paths,
                              const Amino::Array<Amino::String>& exclude_paths)
    USDNODE_DOC_ICON_X("get_or_create_collection",
                       "USD_Collection_get_or_create_collection.md",
                       "usd_default.svg",
                       "outName=success");

USD_NODEDEF_DECL
void get_all_collection_names(
    const BifrostUsd::Prim&                         prim,
    Amino::MutablePtr<Amino::Array<Amino::String>>& names)
    USDNODE_DOC_ICON("get_all_collection_names",
                     "USD_Collection_get_all_collection_names.md",
                     "usd_default.svg");

USD_NODEDEF_DECL
void get_includes_paths(const BifrostUsd::Prim& prim,
                        const Amino::String&    collection_name,
                        Amino::MutablePtr<Amino::Array<Amino::String>>& paths)
    USDNODE_DOC_ICON("get_includes_paths",
                     "USD_Collection_get_includes_paths.md",
                     "usd_default.svg");

USD_NODEDEF_DECL
void get_excludes_paths(const BifrostUsd::Prim& prim,
                        const Amino::String&    collection_name,
                        Amino::MutablePtr<Amino::Array<Amino::String>>& paths)
    USDNODE_DOC_ICON("get_excludes_paths",
                     "USD_Collection_get_excludes_paths.md",
                     "usd_default.svg");

} // namespace Collection
} // namespace USD

#endif // USD_COLLECTION_NODEDEFS_H
