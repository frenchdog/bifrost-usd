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

#ifndef BIFROST_HD_TEST_SCENE_INDEX_PRIM_H
#define BIFROST_HD_TEST_SCENE_INDEX_PRIM_H

#include <gtest/gtest.h>

#include "Export.h"
#include "RecordingSceneIndexObserver.h"

#include <pxr/imaging/hd/sceneIndex.h>
#include <pxr/usd/usd/stage.h>
#include <pxr/usd/usdGeom/tokens.h>
#include <pxr/usdImaging/usdImaging/tokens.h>
#include <pxr/usdImaging/usdImagingGL/engine.h>

using UsdImagingGLEngineSharedPtr =
    std::shared_ptr<class PXR_NS::UsdImagingGLEngine>;

namespace BifrostHdTest {

class BIFROST_HD_TESTUTILS_SHARED_DECL TestSceneIndexPrim
    : public ::testing::Test {
protected:
    /// \brief Method that is called before a unit test is executed.
    void SetUp() override;

    /// \brief Method that is called after a unit test is executed.
    void TearDown() override;

    bool openStage(const std::string& stageFilePath);

    bool render();

    void reRender();

    PXR_NS::UsdPrim getUsdPrim(const PXR_NS::SdfPath& primPath);

    PXR_NS::HdSceneIndexPrim getHdPrim(
        const PXR_NS::SdfPath& bifrostProcPrimPath);

    PXR_NS::HdSceneIndexBaseRefPtr getSceneIndex() const;

    RecordingSceneIndexObserver& getObserver();

    static void ExportAsString(const PXR_NS::HdSceneIndexPrim& prim,
                               const std::string&              filePath = "");

    static void TestHdSceneIndexMesh(const PXR_NS::HdSceneIndexPrim& prim,
                                     bool hasDisplayColor = true);

    static void TestHdSceneIndexBasisCurves(
        const PXR_NS::HdSceneIndexPrim& prim);

private:
    PXR_NS::UsdStageRefPtr         m_stage;
    UsdImagingGLEngineSharedPtr    m_engine;
    PXR_NS::HdSceneIndexBaseRefPtr m_sceneIndex;
    RecordingSceneIndexObserver    m_observer;
};

} // namespace BifrostHdTest

#endif // BIFROST_HD_TEST_SCENE_INDEX_PRIM_H
