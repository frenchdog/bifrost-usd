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

#include <BifrostHydra/Engine/JobTranslationData.h>

#include <BifrostHydra/Engine/Parameters.h>

namespace BifrostHd {

class JobTranslationData::Impl {
public:
    Impl(Parameters& params, const Time& time)
        : m_params(params), m_time(time) {}

    Parameters&              getParameters() { return m_params; }
    JobTranslationData::Time getTime() const { return m_time; }

private:
    Parameters& m_params;
    Time        m_time;
};

JobTranslationData::JobTranslationData(Parameters& params, const Time& time)
    : m_impl(std::make_unique<Impl>(params, time)) {}

JobTranslationData::~JobTranslationData() = default;

Parameters& JobTranslationData::getParameters() {
    return m_impl->getParameters();
}

JobTranslationData::Time JobTranslationData::getTime() const {
    return m_impl->getTime();
}

} // namespace BifrostHd
