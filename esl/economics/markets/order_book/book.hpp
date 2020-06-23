/// \file   book.hpp
///
/// \brief
///
/// \authors    Maarten P. Scholl
/// \date       2020-04-05
/// \copyright  Copyright 2017-2020 The Institute for New Economic Thinking,
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


#ifndef ME_ORDER_BOOK_HPP
#define ME_ORDER_BOOK_HPP

#include <map>
#include <queue>
#include <string>


#include <esl/economics/markets/order_book/order.hpp>


namespace esl::economics::markets::order_book {

    class book
    {
    public:
        bool insert(const order &order);

        void erase(const order &order);

        order &find(order::side_t side, const esl::identity<esl::law::property>& id);

        bool match(std::queue<order> &);

        [[nodiscard]] price spread() const
        {
            return orders_ask.cbegin()->first - orders_bid.cbegin() ->first;
        }

        void match(order &bid, order &ask);


        typedef std::multimap<price, order, std::greater<>> bid_t;
        typedef std::multimap<price, order, std::less<>> ask_t;


        bid_t orders_bid;
        ask_t orders_ask;
    };
}  // namespace esl::economics::markets::order_book


#endif  // ME_ORDER_BOOK_HPP
