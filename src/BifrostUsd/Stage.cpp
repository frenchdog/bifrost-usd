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

#include <BifrostUsd/Layer.h>
#include <BifrostUsd/Stage.h>

#include <Amino/Core/String.h>
#include <Amino/Cpp/ClassDefine.h>

// Note: To silence warnings coming from USD library
#include <bifusd/config/CfgWarningMacros.h>
BIFUSD_WARNING_PUSH

BIFUSD_WARNING_DISABLE_MSC(4003)
BIFUSD_WARNING_DISABLE_MSC(4244)
BIFUSD_WARNING_DISABLE_MSC(4305)
BIFUSD_WARNING_DISABLE_MSC(4800)

#include <pxr/usd/usd/attribute.h>
#include <pxr/usd/usd/editContext.h>
#include <pxr/usd/usd/prim.h>
#include <pxr/usd/usd/stage.h>

/// \todo BIFROST-6874 remove PXR_NS::Work_EnsureDetachedTaskProgress();
#include <pxr/base/work/detachedTask.h>

BIFUSD_WARNING_POP


namespace {

PXR_NS::UsdStage::InitialLoadSet GetPxrInitialLoadSet(
    BifrostUsd::InitialLoadSet load) {
    return load == BifrostUsd::InitialLoadSet::LoadAll
               ? PXR_NS::UsdStage::InitialLoadSet::LoadAll
               : PXR_NS::UsdStage::InitialLoadSet::LoadNone;
}

} // namespace

namespace BifrostUsd {

Stage::Stage()
    : m_rootLayer(Amino::newClassPtr<Layer>()),
      m_stage(PXR_NS::UsdStage::Open(m_rootLayer->m_layer)) {}

Stage::Stage(Invalid) { assert(!isValid()); }

Stage::Stage(const Layer& rootLayer, const InitialLoadSet load)
    : m_rootLayer(Amino::newClassPtr<Layer>(rootLayer)),
      m_stage(
          PXR_NS::UsdStage::Open(m_rootLayer->m_layer, GetPxrInitialLoadSet(load)))

{}

Stage::Stage(const Layer&                       rootLayer,
             const PXR_NS::UsdStagePopulationMask& mask,
             const InitialLoadSet               load)
    : m_rootLayer(Amino::newClassPtr<Layer>(rootLayer)),
      m_stage(PXR_NS::UsdStage::OpenMasked(
          m_rootLayer->m_layer, mask, GetPxrInitialLoadSet(load)))

{}

Stage::Stage(const Amino::String& filePath, const InitialLoadSet load)
    : m_rootLayer(Amino::newClassPtr<Layer>(filePath, "")),
      m_stage(PXR_NS::UsdStage::Open(m_rootLayer->m_layer,
                                  GetPxrInitialLoadSet(load))) {}

Stage::Stage(const Amino::String&               filePath,
             const PXR_NS::UsdStagePopulationMask& mask,
             const InitialLoadSet               load)
    : m_rootLayer(Amino::newClassPtr<Layer>(filePath, "")),
      m_stage(PXR_NS::UsdStage::OpenMasked(
          m_rootLayer->m_layer, mask, GetPxrInitialLoadSet(load))) {}

Stage::Stage(const Stage& other) : Stage(*other.m_rootLayer) {
    // The newly created UsdStage has the root layer as its default EditTarget.
    // We can't just copy the m_editLayerIndex, but must set the desired
    // layer as the EditTarget:
    setEditLayerIndex(other.m_editLayerIndex, true);

    last_modified_prim             = other.last_modified_prim;
    m_variantSelection = other.m_variantSelection;
}

Stage& Stage::operator=(const Stage& other) {
    m_rootLayer = Amino::newClassPtr<Layer>(*other.m_rootLayer);
    m_stage     = PXR_NS::UsdStage::Open(m_rootLayer->m_layer);

    // The newly created UsdStage has the root layer as its default EditTarget.
    // We can't just copy the m_editLayerIndex, but must set the desired
    // layer as the EditTarget:
    setEditLayerIndex(other.m_editLayerIndex, true);

    last_modified_prim             = other.last_modified_prim;
    m_variantSelection = other.m_variantSelection;

    return *this;
}

Stage::Stage(Stage&& other) noexcept { *this = std::move(other); }

bool Stage::setEditLayerIndex(const int layerIndex,
                              bool      defaultToRoot) {
    if (!isValid())
        return false;
    if (layerIndex >= 0) {
        auto subLayerPaths = m_stage->GetRootLayer()->GetSubLayerPaths();
        const size_t numLayers = subLayerPaths.size();
        if (static_cast<size_t>(layerIndex) < numLayers) {
            // Find the sublayer
            auto layer = PXR_NS::SdfLayer::FindOrOpen(subLayerPaths[layerIndex]);
            if (layer) {
                m_stage->SetEditTarget(layer);
                m_editLayerIndex = layerIndex;
                return true;
            }
        }
    }

    if (layerIndex == -1 || defaultToRoot) {
        auto layer = m_stage->GetRootLayer();
        m_stage->SetEditTarget(layer);
        m_editLayerIndex = -1;
        return true;
    }
    return false;
}

bool Stage::save(const Amino::String& filePath) const {
    return m_rootLayer->exportToFile(filePath.c_str());
}

Amino::String Stage::lastModifiedVariantSet() const {
    if (m_variantSelection.empty()) {
        return Amino::String{};
    }
    return m_variantSelection.variantSet();
}

Amino::String Stage::lastModifiedVariant() const {
    if (m_variantSelection.empty()) {
        return Amino::String{};
    }
    return m_variantSelection.variant();
}

//------------------------------------------------------------------------------
//
namespace {
Amino::Ptr<BifrostUsd::Stage> createDefaultStage() {
    // Destructor of USD instances are lauching threads. This result in
    // a deadlock on windows when unloading the library (which destroys the
    // default constructed object held in static variables).
    /// \todo BIFROST-6874 remove PXR_NS::Work_EnsureDetachedTaskProgress();
    PXR_NS::Work_EnsureDetachedTaskProgress();
    return Amino::newClassPtr<BifrostUsd::Stage>();
}
} // namespace
} // namespace BifrostUsd

AMINO_DEFINE_DEFAULT_CLASS(BifrostUsd::Stage, BifrostUsd::createDefaultStage());
