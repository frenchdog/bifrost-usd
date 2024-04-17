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
/// \file  VariantSelection.h
/// \brief Store current variantSet of the Bifrost USD Stage.

#ifndef ADSK_USD_VARIANTSELECTION_H
#define ADSK_USD_VARIANTSELECTION_H

#include "BifrostUsdExport.h"

#include <Amino/Core/String.h>

#include <vector>

namespace BifrostUsd {

/// \class VariantSelection VariantSelection.h
/// \brief Record the current stage variants selection.
///
/// This class stores a stack of "VariantSet name" and "Variant name" pair.
/// It is instanced by a BifrostUsd::Stage and authored in the following
/// operators:
/// - USD::VariantSet::add_variant
/// - USD::VariantSet::set_variant_selection
///
/// Special case:
/// USD allows adding a variantSet with the same name than the variantSet of
/// the stage's current EditTarget. Bifrost USD does not allow it.
/// This is because nested variantSet with same name are confusing for several
/// applications. Thus when adding a selection in a
/// BifrostUsd::VariantSelection, if the previous selection has the same
/// variantSet name, it will override it.
class USD_DECL VariantSelection {
public:
    using PairOfNames    = std::pair<Amino::String, Amino::String>;
    using SelectionStack = std::vector<PairOfNames>;

public:
    VariantSelection() = default;

    /// \brief Get the path of the prim of the currently selected VariantSet.
    ///
    /// \return The path of the prim.
    Amino::String const& primPath() const { return m_primPath; }

    /// \brief Set the path of the prim of the currently selected VariantSet.
    void setPrimPath(const Amino::String& primPath);

    /// \brief Get the stack of VariantSet name and Variant name pairs.
    SelectionStack const& stack() const { return m_stack; }

    /// \brief Empty if not prim path and an empty stack.
    bool empty() const { return m_primPath.empty() && m_stack.empty(); }

    /// \brief Get the name of the currently selected VariantSet.
    Amino::String const& variantSet() const { return m_stack.back().first; }

    /// \brief Get the name of the current variant.
    Amino::String const& variant() const { return m_stack.back().second; }

    /// \brief Get variant selection info with this formatting:
    /// on prim:     /myPrim
    /// variant 0 :  myVariantSetA/variantA
    /// selection :      myNestedVariantSet/variantB
    Amino::String variantInfo() const;

    /// \brief Add a new variant selection to the VariantSelection stack.
    /// If the last element of the stack has the same variantSet name, it will
    /// be replaced by the new one.
    void add(const Amino::String& primPath,
             const Amino::String& variantSetName,
             const Amino::String& variantName = "");

    /// \brief Empty the VariantSelection stack.
    void clear();

    bool operator==(VariantSelection const& rhs) const;

private:
    Amino::String  m_primPath;
    SelectionStack m_stack;
};

} // namespace BifrostUsd

#endif // ADSK_USD_VARIANTSELECTION_H
