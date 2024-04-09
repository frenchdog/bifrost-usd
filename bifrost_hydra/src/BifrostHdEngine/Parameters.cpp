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

#include <BifrostHydra/Engine/Parameters.h>

#include <Bifrost/Object/Object.h>

#include <Amino/Core/Array.h>
#include <Amino/Core/Ptr.h>

#include <pxr/imaging/hd/primvarsSchema.h>

namespace BifrostHd {

class Parameters::Impl {
public:
    Impl() = default;

    ~Impl() = default;

    void setInputScene(PXR_NS::HdSceneIndexBaseRefPtr inputScene) {
        m_inputScene = std::move(inputScene);
    }

    PXR_NS::HdSceneIndexBaseRefPtr inputScene() const {
        return m_inputScene;
    }

    void setInputs(const PXR_NS::HdSceneIndexPrim& prim) {
        auto primvarSchema =
            PXR_NS::HdPrimvarsSchema::GetFromParent(prim.dataSource);

        for (const auto& name : primvarSchema.GetPrimvarNames()) {
            if (name == "hdGp:proceduralType") {
                continue;
            }

            if (auto dataSource =
                    primvarSchema.GetPrimvar(name).GetPrimvarValue()) {
                auto value = dataSource->GetValue(0.0f);
                if (name == "bifrost:graph") {
                    if (value.IsHolding<PXR_NS::TfToken>()) {
                        const auto& graphName  = value.UncheckedGet<PXR_NS::TfToken>();
                        m_compound_name = graphName.GetText();
                    }
                } else if (name == "bifrost:output") {
                    if (value.GetTypeName() == "string") {
                        auto output_name = value.UncheckedGet<std::string>();
                        auto objectArray = Amino::Array<Amino::Ptr<Bifrost::Object>>();
                        m_output         = std::make_pair(output_name, objectArray);
                    }
                } else {
                    m_inputs[name.GetText()] = dataSource->GetValue(0.0f);
                }
            }
        }
    }

    const std::string& compoundName() const { return m_compound_name; }

    const Inputs& inputs() const { return m_inputs; }
    Inputs& inputs() { return m_inputs; }

    const Output& output() const { return m_output; }
    Output& output() { return m_output; }

public:
    /// Disabled
    /// \{
    Impl(const Impl&)             = delete;
    Impl(const Impl&&)            = delete;
    Impl& operator=(const Impl&)  = delete;
    Impl& operator=(const Impl&&) = delete;
    /// \}

private:
    std::string                    m_compound_name;
    PXR_NS::HdSceneIndexBaseRefPtr m_inputScene;
    Inputs                         m_inputs;
    Output                         m_output;
};

Parameters::Parameters() : m_impl(std::make_unique<Impl>()) {}

Parameters::~Parameters() = default;

PXR_NS::HdSceneIndexBaseRefPtr Parameters::inputScene() const {
    return m_impl->inputScene();
}
void Parameters::setInputScene(PXR_NS::HdSceneIndexBaseRefPtr inputScene) {
    m_impl->setInputScene(std::move(inputScene));
}

void Parameters::setInputs(const PXR_NS::HdSceneIndexPrim& prim) {
    m_impl->setInputs(prim);
}

const std::string& Parameters::compoundName() const { return m_impl->compoundName(); }

const Inputs& Parameters::inputs() const { return m_impl->inputs(); }

Inputs& Parameters::inputs() { return m_impl->inputs(); }

const Output& Parameters::output() const { return m_impl->output(); }

Output& Parameters::output() { return m_impl->output(); }

} // namespace BifrostHd
