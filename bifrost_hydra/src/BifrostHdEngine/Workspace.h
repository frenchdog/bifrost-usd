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

#ifndef BIFROST_HD_ENGINE_WORKSPACE_H_
#define BIFROST_HD_ENGINE_WORKSPACE_H_

#include <BifrostHydra/Engine/Export.h>

#include <BifrostGraph/Executor/Workspace.h>

#include <Amino/Core/String.h>

namespace BifrostHd {

class BIFROST_HD_ENGINE_SHARED_DECL Workspace final
    : public BifrostGraph::Executor::Workspace {
public:
    explicit Workspace(const Amino::String& name);
    ~Workspace() override;

    void onReportedMessage(BifrostGraph::Executor::MessageSource   source,
                           BifrostGraph::Executor::MessageCategory category,
                           const Amino::String&                    message) const noexcept override;

    const BifrostGraph::Executor::StringArray& getMessages() const {
        return m_messages;
    }
    bool hasMessages() const { return !m_messages.empty(); }
    void clearMessages() { m_messages.clear(); }

private:
    // Store all reported messages. This is used for testing.
    mutable BifrostGraph::Executor::StringArray m_messages;
};

} // namespace BifrostHd

#endif // BIFROST_HD_ENGINE_WORKSPACE_H_
