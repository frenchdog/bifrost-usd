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

#ifndef BIFROST_HD_ENGINE_VALUE_TRANSLATION_DATA_H
#define BIFROST_HD_ENGINE_VALUE_TRANSLATION_DATA_H

#include <BifrostHydra/Engine/Export.h>

#include <BifrostGraph/Executor/TypeTranslation.h>

#include <Amino/Core/Any.h>

#include <string>

namespace BifrostHd {

class JobTranslationData;

/// \brief Specialization of Bifrost TypeTranslation::ValueData for graph inputs.
///
/// This class holds the data that will be passed to the Job's setInputValue()
/// method, and the Job will pass it to the TypeTranslation table.
///
/// See BifrostGraph::Executor::Job::setInputValue()
/// \see BifrostHd::TypeTranslation::convertValueFromHost()
class BIFROST_HD_ENGINE_SHARED_DECL InputValueData final
    : public BifrostGraph::Executor::TypeTranslation::ValueData {
public:
    InputValueData(JobTranslationData& jobTranslationData,
                   std::string         name,
                   Amino::Any          defaultVal);
    ~InputValueData() override;

    Amino::Any                getInput() const;
    const JobTranslationData& jobTranslationData() const;

public:
    /// Disabled
    /// \{
    InputValueData(const InputValueData&)            = delete;
    InputValueData(InputValueData&&)                 = delete;
    InputValueData& operator=(const InputValueData&) = delete;
    InputValueData& operator=(InputValueData&&)      = delete;
    /// \}

private:
    JobTranslationData& m_jobTranslationData;
    std::string         m_name;
    Amino::Any          m_defaultVal;
};

/// \brief Specialization of Bifrost TypeTranslation::ValueData for graph outputs.
///
/// This class holds the data that will be passed to the Job's getOutputValue()
/// method, and the Job will pass it to the TypeTranslation table.
///
/// See BifrostGraph::Executor::Job::getOutputValue()
/// \see BifrostHd::TypeTranslation::convertValueToHost()
class BIFROST_HD_ENGINE_SHARED_DECL OutputValueData final
    : public BifrostGraph::Executor::TypeTranslation::ValueData {
public:
    OutputValueData(JobTranslationData& jobTranslationData, std::string name);
    ~OutputValueData() override;

    bool                      setOutput(const Amino::Any& value);
    const JobTranslationData& jobTranslationData() const;

public:
    /// Disabled
    /// \{
    OutputValueData(const OutputValueData&)            = delete;
    OutputValueData(OutputValueData&&)                 = delete;
    OutputValueData& operator=(const OutputValueData&) = delete;
    OutputValueData& operator=(OutputValueData&&)      = delete;
    /// \}

private:
    JobTranslationData& m_jobTranslationData;
    std::string         m_name;
};

} // namespace BifrostHd

#endif // BIFROST_HD_ENGINE_VALUE_TRANSLATION_DATA_H
