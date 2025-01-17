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

#include "TestSceneIndexPrim.h"

#include <pxr/imaging/hd/basisCurvesSchema.h>
#include <pxr/imaging/hd/meshSchema.h>
#include <pxr/imaging/hd/primvarsSchema.h>
#include <pxr/imaging/hd/sceneIndexPluginRegistry.h>
#include <pxr/imaging/hd/xformSchema.h>
#include <pxr/usd/usd/prim.h>

#include <cassert>
#include <fstream>

#if defined(_WIN32)
#include <Windows.h>

#pragma comment(lib, "User32.lib")
#pragma comment(lib, "Gdi32.lib")
#pragma comment(lib, "Opengl32.lib")
#endif

PXR_NAMESPACE_USING_DIRECTIVE

namespace BifrostHdTest {

void TestSceneIndexPrim::SetUp() {
#if defined(_WIN32)
    WNDCLASS wc;
    ZeroMemory(&wc, sizeof(wc));
    wc.style         = CS_HREDRAW | CS_VREDRAW | CS_OWNDC;
    wc.lpfnWndProc   = (WNDPROC)DefWindowProc;
    wc.lpszClassName = "BifrostHydra_dummy";

    RegisterClass(&wc);

    HWND hWnd =
        CreateWindowEx(0, wc.lpszClassName, "BifrostHydra",
                       WS_CLIPSIBLINGS | WS_CLIPCHILDREN | WS_OVERLAPPEDWINDOW,
                       CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT,
                       CW_USEDEFAULT, nullptr, nullptr, nullptr, nullptr);
    assert(hWnd);

    HDC hDC = GetDC(hWnd);
    assert(hDC);

    // clang-format off
    PIXELFORMATDESCRIPTOR pfd = {
        sizeof(PIXELFORMATDESCRIPTOR),  // Size Of This Pixel Format Descriptor
        1,                              // Version Number
        PFD_DRAW_TO_WINDOW |            // Format Must Support Window
        PFD_SUPPORT_OPENGL |            // Format Must Support OpenGL
        PFD_DOUBLEBUFFER,               // Must Support Double Buffering
        PFD_TYPE_RGBA,                  // Request An RGBA Format
        16,                             // Select Our Color Depth
        0, 0, 0, 0, 0, 0,               // Color Bits Ignored
        0,                              // No Alpha Buffer
        0,                              // Shift Bit Ignored
        0,                              // No Accumulation Buffer
        0, 0, 0, 0,                     // Accumulation Bits Ignored
        16,                             // 16Bit Z-Buffer (Depth Buffer)
        0,                              // No Stencil Buffer
        0,                              // No Auxiliary Buffer
        PFD_MAIN_PLANE,                 // Main Drawing Layer
        0,                              // Reserved
        0, 0, 0                         // Layer Masks Ignored
    };
    // clang-format on

    int pixelFormat = ChoosePixelFormat(hDC, &pfd);
    SetPixelFormat(hDC, pixelFormat, &pfd);

    HGLRC hRC = wglCreateContext(hDC);
    assert(hRC);
    wglMakeCurrent(hDC, hRC);
#endif
}

void TestSceneIndexPrim::TearDown() {}

bool TestSceneIndexPrim::openStage(const std::string& stageFilePath) {
    m_stage = UsdStage::Open(stageFilePath);
    return m_stage;
}

bool TestSceneIndexPrim::render() {
    if (!m_stage) {
        return false;
    }
    // render the scene
    SdfPathVector excludedPaths;

    UsdImagingGLRenderParams params;
    params.frame = 1;

    m_engine.reset(new UsdImagingGLEngine(m_stage->GetPseudoRoot().GetPath(),
                                          excludedPaths));

    m_engine->Render(m_stage->GetPseudoRoot(), params);

    auto registeredSceneIndexNames =
        HdSceneIndexNameRegistry::GetInstance().GetRegisteredNames();

    m_sceneIndex = HdSceneIndexNameRegistry::GetInstance().GetNamedSceneIndex(
        registeredSceneIndexNames[0]);
    if (m_sceneIndex) {
        m_sceneIndex->AddObserver(HdSceneIndexObserverPtr(&m_observer));
        return true;
    }
    return false;
}

void TestSceneIndexPrim::reRender() {
    UsdImagingGLRenderParams params;
    params.frame = 1;
    m_observer.Clear();
    return m_engine->Render(m_stage->GetPseudoRoot(), params);
}

PXR_NS::UsdPrim TestSceneIndexPrim::getUsdPrim(
    const PXR_NS::SdfPath& primPath) {
    return m_stage->GetPrimAtPath(primPath);
}

HdSceneIndexPrim TestSceneIndexPrim::getHdPrim(
    const SdfPath& bifrostProcPrimPath) {
    return m_sceneIndex->GetPrim(bifrostProcPrimPath);
}

PXR_NS::HdSceneIndexBaseRefPtr TestSceneIndexPrim::getSceneIndex() const {
    return m_sceneIndex;
}

RecordingSceneIndexObserver& TestSceneIndexPrim::getObserver() {
    return m_observer;
}

// static
void TestSceneIndexPrim::TestHdSceneIndexMesh(
    const PXR_NS::HdSceneIndexPrim& prim, bool hasDisplayColor) {
    EXPECT_EQ(prim.primType, HdPrimTypeTokens->mesh);
    EXPECT_EQ(prim.primType, HdPrimTypeTokens->mesh);
    auto names = prim.dataSource->GetNames();
    EXPECT_EQ(names.size(), 3);
    EXPECT_EQ(names[0], HdMeshSchemaTokens->mesh);
    EXPECT_EQ(names[1], HdPrimvarsSchemaTokens->primvars);
    EXPECT_EQ(names[2], HdXformSchemaTokens->xform);
    auto meshSchema = HdMeshSchema::GetFromParent(prim.dataSource);
    HdMeshTopologySchema meshTopologySchema = meshSchema.GetTopology();
    EXPECT_TRUE(meshTopologySchema.IsDefined());
    const auto& faceVertexCountsDataSource =
        meshTopologySchema.GetFaceVertexCounts();
    EXPECT_TRUE(faceVertexCountsDataSource);
    const auto& faceVertexIndicesDataSource =
        meshTopologySchema.GetFaceVertexIndices();
    EXPECT_TRUE(faceVertexIndicesDataSource);

    auto primvarsSchema = HdPrimvarsSchema::GetFromParent(prim.dataSource);
    EXPECT_TRUE(primvarsSchema.IsDefined());
    EXPECT_TRUE(!primvarsSchema.GetPrimvarNames().empty());
    EXPECT_EQ(primvarsSchema.GetPrimvarNames()[0],
              HdPrimvarsSchemaTokens->points);
    auto ptsPv = primvarsSchema.GetPrimvar(HdPrimvarsSchemaTokens->points);
    auto ptsPrimvarValue = ptsPv.GetPrimvarValue();
    EXPECT_TRUE(ptsPrimvarValue);
    VtValue ptsValue = ptsPrimvarValue->GetValue(0.0f);
    EXPECT_TRUE(ptsValue.IsHolding<VtVec3fArray>());
    const auto& ptsArray = ptsValue.UncheckedGet<VtVec3fArray>();
    EXPECT_EQ(ptsArray.size(), 8);
    EXPECT_EQ(ptsPv.GetInterpolation()->GetTypedValue(0.0f),
              HdPrimvarSchemaTokens->vertex);

    if (!hasDisplayColor) {
        return;
    }

    EXPECT_EQ(primvarsSchema.GetPrimvarNames().size(), 2);
    EXPECT_EQ(primvarsSchema.GetPrimvarNames()[1], HdTokens->displayColor);
    auto dcPv           = primvarsSchema.GetPrimvar(HdTokens->displayColor);
    auto dcPrimvarValue = dcPv.GetPrimvarValue();
    EXPECT_TRUE(dcPrimvarValue);
    VtValue dcValue = dcPrimvarValue->GetValue(0.0f);
    EXPECT_TRUE(dcValue.IsHolding<VtVec3fArray>());
    const auto& dcArray = dcValue.UncheckedGet<VtVec3fArray>();
    EXPECT_EQ(dcArray.size(), 24);
    EXPECT_EQ(dcPv.GetInterpolation()->GetTypedValue(0.0f),
              HdPrimvarSchemaTokens->faceVarying);
}

// static
void TestSceneIndexPrim::TestHdSceneIndexBasisCurves(
    const PXR_NS::HdSceneIndexPrim& prim) {
    EXPECT_EQ(prim.primType, HdPrimTypeTokens->basisCurves);

    auto names = prim.dataSource->GetNames();
    EXPECT_EQ(names.size(), 3);
    EXPECT_EQ(names[0], HdBasisCurvesSchemaTokens->basisCurves);
    EXPECT_EQ(names[1], HdPrimvarsSchemaTokens->primvars);
    EXPECT_EQ(names[2], HdXformSchemaTokens->xform);

    auto basisCurveSchema = HdBasisCurvesSchema::GetFromParent(prim.dataSource);
    auto topologySchema   = basisCurveSchema.GetTopology();
    EXPECT_TRUE(topologySchema.IsDefined());

    const auto& cvcDs = topologySchema.GetCurveVertexCounts();
    EXPECT_TRUE(cvcDs);

    const auto& ciDs = topologySchema.GetCurveIndices();
    EXPECT_TRUE(ciDs);

    auto primvarsSchema = HdPrimvarsSchema::GetFromParent(prim.dataSource);
    EXPECT_TRUE(primvarsSchema.IsDefined());
    EXPECT_EQ(primvarsSchema.GetPrimvarNames().size(), 3);
    EXPECT_EQ(primvarsSchema.GetPrimvarNames()[0], HdTokens->displayColor);
    auto dcPv           = primvarsSchema.GetPrimvar(HdTokens->displayColor);
    auto dcPrimvarValue = dcPv.GetPrimvarValue();
    EXPECT_TRUE(dcPrimvarValue);
    VtValue dcValue = dcPrimvarValue->GetValue(0.0f);
    EXPECT_TRUE(dcValue.IsHolding<VtVec3fArray>());
    const auto& dcArray = dcValue.UncheckedGet<VtVec3fArray>();
    EXPECT_EQ(dcArray.size(), 18);
    EXPECT_EQ(dcPv.GetInterpolation()->GetTypedValue(0.0f),
              HdPrimvarSchemaTokens->varying);

    auto ptsPv = primvarsSchema.GetPrimvar(HdPrimvarsSchemaTokens->points);
    auto ptsPrimvarValue = ptsPv.GetPrimvarValue();
    EXPECT_TRUE(ptsPrimvarValue);
    VtValue ptsValue = ptsPrimvarValue->GetValue(0.0f);
    EXPECT_TRUE(ptsValue.IsHolding<VtVec3fArray>());
    const auto& ptsArray = ptsValue.UncheckedGet<VtVec3fArray>();
    EXPECT_EQ(ptsArray.size(), 18);
    EXPECT_EQ(ptsPv.GetInterpolation()->GetTypedValue(0.0f),
              HdPrimvarSchemaTokens->vertex);
}

namespace {

std::string dataSourceToString(const HdDataSourceBaseHandle& dataSource,
                               int&                          depth) {
    std::string str;

    std::string prefix;
    for (int i = 0; i < depth; ++i) {
        prefix += "    ";
    }
    depth++;

    auto container = HdContainerDataSource::Cast(dataSource);
    if (!container) {
        auto vector = HdVectorDataSource::Cast(dataSource);
        if (vector) {
            str += prefix + "is a HdVectorDataSource of size " +
                   std::to_string(vector->GetNumElements()) + "\n";
            for (size_t i = 0; i < vector->GetNumElements(); ++i) {
                auto vecElem = vector->GetElement(i);
                str += dataSourceToString(vecElem, depth);
            }
        }

        auto sample = HdSampledDataSource::Cast(dataSource);
        if (sample) {
            auto value = sample->GetValue(0);
            str += prefix + "is a HdSampledDataSource of type " +
                   value.GetTypeName() + "\n";

            if (value.IsHolding<TfToken>()) {
                const auto& elem = value.UncheckedGet<TfToken>();
                str += prefix + prefix + "value: " + elem.GetString() + "\n";
            }

            else if (value.IsHolding<bool>()) {
                auto elem = value.UncheckedGet<bool>();
                str +=
                    prefix + prefix + "value: " + std::to_string(elem) + "\n";
            }

            else if (value.IsHolding<int>()) {
                auto elem = value.UncheckedGet<int>();
                str +=
                    prefix + prefix + "value: " + std::to_string(elem) + "\n";
            }

            else if (value.IsHolding<VtArray<bool>>()) {
                auto arrayType = value.UncheckedGet<VtArray<bool>>();
                for (auto elem : arrayType) {
                    str += prefix + prefix + "value: " + std::to_string(elem) +
                           "\n";
                }
            }

            else if (value.IsHolding<VtArray<int>>()) {
                auto arrayType = value.UncheckedGet<VtArray<int>>();
                for (auto elem : arrayType) {
                    str += prefix + prefix + "value: " + std::to_string(elem) +
                           "\n";
                }
            }

            else if (value.IsHolding<VtArray<float>>()) {
                auto arrayType = value.UncheckedGet<VtArray<float>>();
                for (auto elem : arrayType) {
                    str += prefix + prefix + "value: " + std::to_string(elem) +
                           "\n";
                }
            }

            else if (value.IsHolding<GfVec3f>()) {
                auto vec3f = value.UncheckedGet<GfVec3f>();

                auto strVec3f = "(" + std::to_string(vec3f[0]) + ", " +
                                std::to_string(vec3f[1]) + ", " +
                                std::to_string(vec3f[2]) + ")";
                str += prefix + prefix + "value: " + strVec3f + "\n";
            }

            else if (value.IsHolding<GfVec3d>()) {
                auto vec3d = value.UncheckedGet<GfVec3d>();

                auto strVec3d = "(" + std::to_string(vec3d[0]) + ", " +
                                std::to_string(vec3d[1]) + ", " +
                                std::to_string(vec3d[2]) + ")";
                str += prefix + prefix + "value: " + strVec3d + "\n";
            }

            else if (value.IsHolding<GfMatrix4d>()) {
                auto mat4d = value.UncheckedGet<GfMatrix4d>();

                double data[4][4];
                mat4d.Get(data);
                auto strMat4d = std::string("(") + "{" +
                                std::to_string(data[0][0]) + ", " +
                                std::to_string(data[0][1]) + ", " +
                                std::to_string(data[0][2]) + ", " +
                                std::to_string(data[0][3]) + "}, " + "{" +
                                std::to_string(data[1][0]) + ", " +
                                std::to_string(data[1][1]) + ", " +
                                std::to_string(data[1][2]) + ", " +
                                std::to_string(data[1][3]) + "}, " + "{" +
                                std::to_string(data[2][0]) + ", " +
                                std::to_string(data[2][1]) + ", " +
                                std::to_string(data[2][2]) + ", " +
                                std::to_string(data[2][3]) + "}, " + "{" +
                                std::to_string(data[3][0]) + ", " +
                                std::to_string(data[3][1]) + ", " +
                                std::to_string(data[3][2]) + ", " +
                                std::to_string(data[3][3]) + "}" + ")";
                str += prefix + prefix + "value: " + strMat4d + "\n";
            }

            else if (value.IsHolding<VtArray<SdfPath>>()) {
                auto arrayType = value.UncheckedGet<VtArray<SdfPath>>();
                for (const auto& elem : arrayType) {
                    str +=
                        prefix + prefix + "value: " + elem.GetString() + "\n";
                }
            }

            else if (value.IsHolding<VtArray<GfVec3f>>()) {
                auto arrayType = value.UncheckedGet<VtArray<GfVec3f>>();
                for (auto elem : arrayType) {
                    auto strVec3f = "(" + std::to_string(elem[0]) + ", " +
                                    std::to_string(elem[1]) + ", " +
                                    std::to_string(elem[2]) + ")";
                    str += prefix + prefix + "value: " + strVec3f + "\n";
                }
            }

            else if (value.IsHolding<VtArray<GfVec3d>>()) {
                auto arrayType = value.UncheckedGet<VtArray<GfVec3d>>();
                for (auto elem : arrayType) {
                    auto strVec3d = "(" + std::to_string(elem[0]) + ", " +
                                    std::to_string(elem[1]) + ", " +
                                    std::to_string(elem[2]) + ")";
                    str += prefix + prefix + "value: " + strVec3d + "\n";
                }
            }

            else if (value.IsHolding<VtArray<GfQuath>>()) {
                auto arrayType = value.UncheckedGet<VtArray<GfQuath>>();
                for (auto elem : arrayType) {
                    auto quathh =
                        "(" + std::to_string(elem.GetReal()) + ", " +
                        std::to_string(elem.GetImaginary()[0]) + ", " +
                        std::to_string(elem.GetImaginary()[1]) + ", " +
                        std::to_string(elem.GetImaginary()[2]) + ")";
                    str += prefix + prefix + "value: " + quathh + "\n";
                }
            }

            else {
                str += "[WARNING ]Type " + value.GetTypeName() +
                       " is not supported\n";
            }
        }
        auto block = HdBlockDataSource::Cast(dataSource);
        if (block) {
            // ???
        }

    } else {
        for (const auto& name : container->GetNames()) {
            str += prefix + name.GetString() + "\n";
            auto childContainer = container->Get(name);
            str += dataSourceToString(container->Get(name), depth);
        }
    }
    depth--;
    return str;
}

} // end namespace

// static
void TestSceneIndexPrim::ExportAsString(const PXR_NS::HdSceneIndexPrim& prim,
                                        const std::string& filePath) {
    (void)filePath;
    int         depth = 0;
    std::string result =
        "*********************************************************************"
        "\n";

    result += "Type: " + prim.primType.GetString() + "\n";

    result += dataSourceToString(prim.dataSource, depth);

    result +=
        "*********************************************************************"
        "\n";

    if (filePath.empty()) {
        std::cout << result;
    } else {
        std::ofstream out(filePath);
        out << result;
        out.close();
    }
}
} // end namespace BifrostHdTest
