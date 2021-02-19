/// \file   market.hpp
///
/// \brief
///
/// \authors    Maarten P. Scholl
/// \date       2020-11-19
/// \copyright  Copyright 2017-2021 The Institute for New Economic Thinking,
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
#ifndef MARKET_ECOLOGY_IMPACT_FUNCTION_MARKET_HPP
#define MARKET_ECOLOGY_IMPACT_FUNCTION_MARKET_HPP

#include <esl/economics/markets/market.hpp>

#include <esl/economics/markets/impact_function/order.hpp>

namespace esl::economics::markets::impact_function {

    ///
    /// \brief  walras::price_setter is a market organizer that tries
    ///         to find clearing prices satisfying Walras' law. For this purpose
    ///         several numerical methods are implemented, some of which benefit
    ///         form automatic differentiation.
    ///
    struct market
    : public esl::economics::market
    {
    private:
    public:
        std::shared_ptr<data::output<std::vector<price>>> output_clearing_prices_;
        std::shared_ptr<data::output<std::vector<uint64_t>>> output_volumes_;

    protected:
        friend class boost::serialization::access;

        explicit market( );

    public:

        std::function<double(double)> impact_function;

        ///
        /// \brief Price setter agent state
        ///
        enum state_t
        { sending_quotes    // the agent sends quotes to all market participants
        , clearing_market   // the agent collects all orders and clears market
        } state;

        law::property_map<quote> traded_properties;

        ///
        /// \details
        /// \param i
        /// \param traded_properties
        explicit market( const identity<market> &i, law::property_map<quote> traded_properties = {});

        ///
        /// \brief
        ///
        /// \param start
        /// \return
        simulation::time_point act( simulation::time_interval step, std::seed_seq &seed) override;


        ///
        /// \brief  Clear the market
        ///
        std::map<identity<law::property>, double> clear_market
            ( const std::unordered_map< identity<agent>
                                      , std::shared_ptr<impact_function::order_message>
                                      > &orders
            , const esl::simulation::time_interval &step
            );

        ///
        /// \return friendly description of the agent mentioning the identifier
        [[nodiscard]] std::string describe() const override
        {
            std::stringstream stream_;
            stream_ << "impact function market " << identifier;
            return stream_.str();
        }

        template<class archive_t>
        void serialize(archive_t & archive, const unsigned int version)
        {
            (void)version;
            archive & BOOST_SERIALIZATION_BASE_OBJECT_NVP(market);
            archive & BOOST_SERIALIZATION_NVP(traded_properties);
            archive & BOOST_SERIALIZATION_NVP(output_clearing_prices_);
            archive & BOOST_SERIALIZATION_NVP(state);
        }
    };

}//namespace


#ifdef WITH_MPI
#include <boost/mpi.hpp>
namespace boost {
    namespace mpi {
        template<>
        struct is_mpi_datatype<esl::economics::markets::walras::price_setter>
        : public mpl::false_
        {};

    }//namespace mpi
}//namespace boost
#endif//WITH_MPI


#endif  // MARKET_ECOLOGY_IMPACT_FUNCTION_MARKET_HPP
