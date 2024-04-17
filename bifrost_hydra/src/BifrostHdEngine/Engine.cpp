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

#include <BifrostHydra/Engine/Engine.h>

#include <BifrostHydra/Engine/JobTranslationData.h>
#include <BifrostHydra/Engine/Parameters.h>
#include <BifrostHydra/Engine/ValueTranslationData.h>
#include <BifrostHydra/Engine/Workspace.h>

#include <BifrostGraph/Executor/Factory.h>
#include <BifrostGraph/Executor/GraphContainer.h>
#include <BifrostGraph/Executor/Job.h>
#include <BifrostGraph/Executor/Owner.h>
#include <BifrostGraph/Executor/Utility.h>

#include <Amino/Core/String.h>

using namespace BifrostGraph::Executor;

namespace BifrostHd {

class Engine::Impl {
public:
    Impl() = default;
    ~Impl() noexcept {
        m_container = nullptr;
        // Let the Workspace delete its GraphContainer
    }

    bool initWorkspace() {
        if (!m_workspace) {
            m_workspace =
                BifrostGraph::Executor::makeOwner<BifrostHd::Workspace>(
                    "BifrostHd");
            if (!m_workspace) {
                return false;
            }
            // Use the environment variables BIFROST_LIB_CONFIG_FILES and
            // BIFROST_DISABLE_PACKS to determine the required Bifrost resources
            // to be loaded.
            auto configEnv = BifrostGraph::Executor::makeOwner<
                BifrostGraph::Executor::Utility::ConfigEnv>();
            if (!configEnv) {
                return false;
            }
            if (!m_workspace->loadConfigFiles(configEnv->values("bifrost_pack_config_files"),
                                              configEnv->values("bifrost_disable_packs"))) {
                return false;
            }
        }
        return true;
    }

    BifrostHd::Workspace* getWorkspace() {
        if (!initWorkspace()) {
            return nullptr;
        }
        return m_workspace.get();
    }

    bool initContainer() {
        assert(m_workspace);
        if (!m_container) {
            // Add a single GraphContainer within our Workspace:
            BifrostGraph::Executor::GraphContainer& container =
                m_workspace->addGraphContainer();
            if (!container.isValid()) {
                return false;
            }
            m_container = &container;

            // Since for now we can't change the 'graph topology' at runtime
            // (like connect/disconnect/add node) because there is no Bifrost
            // Graph Editor "attached" to our engine, then loading of
            // the graph and compiling it should happen just once.
            Amino::String name{m_parameters.compoundName().c_str()};
            if (!m_container->setGraph(name)) {
                return false;
            }
            auto status = m_container->compile(GraphCompilationMode::kInit);
            if (status == GraphCompilationStatus::kFailure) {
                // Note that in order to compile/run the graph, none of its
                // inputs/outputs can have its type set to 'auto'.
                // See BIFROST-3651.
                return false;
            }
        }
        return true;
    }

    void setInputScene(PXR_NS::HdSceneIndexBaseRefPtr inputScene) {
        m_parameters.setInputScene(std::move(inputScene));
    }

    void setInputs(const PXR_NS::HdSceneIndexPrim& prim) {
        m_parameters.setInputs(prim);
    }

    bool execute(const double frame) {
        if (!initWorkspace() || !initContainer()) {
            return false;
        }
        Job& job = m_container->getJob();
        if (!job.isValid()) {
            return false;
        }

        // Prepare input values
        const double                  currentTime = frame / m_fps;
        const double                  frameLength = 1.0 / m_fps;
        BifrostHd::JobTranslationData jobData{
            m_parameters,
            /*Time data*/ {currentTime, frame, frameLength}};

        // Set inputs.
        // For each input, the Executor will call convertValueFromHost() on
        // our TypeTranslation class.
        for (const auto& input : job.getInputs()) {
            InputValueData inputData(jobData, input.name.c_str(), input.defaultValue);
            job.setInputValue(input, &inputData);
        }

        // Execute the graph
        auto status  = job.execute();
        bool success = status == JobExecutionStatus::kSuccess;

        if (success) {
            // Get outputs.
            // For each output, the Executor will call convertValueToHost() on
            // our TypeTranslation class.
            for (const auto& output : job.getOutputs()) {
                OutputValueData outputData(jobData, output.name.c_str());
                job.getOutputValue(output, &outputData);
            }
        }

        return success;
    }

    const Output& getOutput() const { return m_parameters.output(); }

private:
    BifrostGraph::Executor::Owner<BifrostHd::Workspace> m_workspace{};
    BifrostGraph::Executor::GraphContainer*             m_container{nullptr};

    double     m_fps{24.0};
    Parameters m_parameters;
};

Engine::Engine() : m_impl(std::make_unique<Impl>()) {}

Engine::~Engine() = default;

BifrostHd::Workspace* Engine::getWorkspace() { return m_impl->getWorkspace(); }

void Engine::setInputScene(PXR_NS::HdSceneIndexBaseRefPtr inputScene) {
    m_impl->setInputScene(std::move(inputScene));
}

void Engine::setInputs(const PXR_NS::HdSceneIndexPrim& prim) {
    m_impl->setInputs(prim);
}

bool Engine::execute(const double frame) { return m_impl->execute(frame); }

const Output& Engine::getOutput() const { return m_impl->getOutput(); }

} // namespace BifrostHd
