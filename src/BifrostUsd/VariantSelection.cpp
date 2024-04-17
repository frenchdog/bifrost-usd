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

#include <BifrostUsd/VariantSelection.h>

#include <algorithm>
#include <string>

namespace BifrostUsd {

void VariantSelection::setPrimPath(const Amino::String& primPath) {
    if (primPath != m_primPath) {
        m_primPath = primPath;
        m_stack.clear();
    }
}

void VariantSelection::add(const Amino::String& primPath,
                            const Amino::String& variantSetName,
                            const Amino::String& variantName) {
    setPrimPath(primPath);
    auto it = std::find_if(m_stack.begin(), m_stack.end(),
                           [&variantSetName](auto const& item) {
                               return item.first == variantSetName;
                           });

    if (it != m_stack.end()) {
        m_stack.resize(std::distance(m_stack.begin(), it));
    }
    m_stack.push_back({variantSetName, variantName});
}

void VariantSelection::clear() {
    m_primPath.clear();
    m_stack.clear();
}

bool VariantSelection::operator==(VariantSelection const& rhs) const {
    if (this->m_primPath != rhs.m_primPath) {
        return false;
    }

    return this->m_stack == rhs.m_stack;
}

Amino::String VariantSelection::variantInfo() const {
    Amino::String path;
    if (!m_stack.empty()) {
        path              = "on prim:     " + m_primPath + "\n";
        size_t stackIndex = 0;
        for (const auto& sel : m_stack) {
            auto tab = Amino::String("  ");
            for (size_t i = 0; i < stackIndex; ++i) {
                tab += "    ";
            }
            if (stackIndex < m_stack.size() - 1) {
                path += Amino::String("variant ") +
                        std::to_string(stackIndex).c_str() + " :";

            } else {
                path += "selection: ";
            }

            path += tab + sel.first + "/" + sel.second + "\n";

            stackIndex++;
        }
        path.pop_back();
    }

    return path;
}

} // namespace BifrostUsd
