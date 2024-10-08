/// \file   version.hpp
///
/// \brief
///
/// \authors    Maarten P Scholl
/// \date       2019-09-01
/// \copyright  Copyright 2017-2919 The Institute for New Economic Thinking,
///             Oxford Martin School, University of Oxford
///
///             Licensed under the Apache License, Version 2.0 (the "License");
///             you may not use this file except in compliance with the License.
///             You may obtain a copy of the License at
///
///                 http://www.apache.org/licenses/LICENSE-2.0
///
///             Unless required by applicable law or agreed to in writing,
///             software distributed under the License is distributed on an "AS
///             IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
///             express or implied. See the License for the specific language
///             governing permissions and limitations under the License.
///
///             You may obtain instructions to fulfill the attribution
///             requirements in CITATION.cff
///
#ifndef ESL_VERSION_HPP
#define ESL_VERSION_HPP

#include <esl/version>

#include <string>

namespace esl {
    constexpr std::string_view version()
    {
        return std::string() + std::to_string(ESL_VERSION_MAJOR) + "." + std::to_string(ESL_VERSION_MINOR) + "." + std::to_string(ESL_VERSION_REVISION);
    }
}// namespace esl

#endif  // ESL_VERSION_HPP
