/// \file   inventory.cpp
///
/// \brief
///
/// \authors    Maarten P. Scholl
/// \date       2019-10-01
/// \copyright  Copyright 2017-2019 The Institute for New Economic Thinking,
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
#include <boost/serialization/export.hpp>
#include <boost/serialization/unordered_map.hpp>
#include <boost/serialization/unordered_set.hpp>
#include <boost/serialization/shared_ptr.hpp>

#include <esl/economics/accounting/inventory.hpp>

//typedef esl::economics::accounting::inventory_by_fungibility<esl::law::property, true> inventory_by_fungibility_p;
//BOOST_CLASS_EXPORT(inventory_by_fungibility_p);

//BOOST_CLASS_EXPORT(esl::economics::accounting::inventory_filter<esl::law::property>)
