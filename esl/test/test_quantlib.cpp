#define BOOST_TEST_MODULE esl_test_quantlib
#include <boost/test/unit_test.hpp>


#include <ql/qldefines.hpp>
#include <ql/instruments/vanillaoption.hpp>
#include <ql/math/integrals/tanhsinhintegral.hpp>
#include <ql/pricingengines/vanilla/analyticeuropeanengine.hpp>
#include <ql/pricingengines/vanilla/analyticeuropeanvasicekengine.hpp>
#include <ql/pricingengines/vanilla/analytichestonengine.hpp>
#include <ql/pricingengines/vanilla/baroneadesiwhaleyengine.hpp>
#include <ql/pricingengines/vanilla/batesengine.hpp>
#include <ql/pricingengines/vanilla/binomialengine.hpp>
#include <ql/pricingengines/vanilla/bjerksundstenslandengine.hpp>
#include <ql/pricingengines/vanilla/fdblackscholesvanillaengine.hpp>
#include <ql/pricingengines/vanilla/integralengine.hpp>
#include <ql/pricingengines/vanilla/mcamericanengine.hpp>
#include <ql/pricingengines/vanilla/mceuropeanengine.hpp>
#include <ql/pricingengines/vanilla/qdfpamericanengine.hpp>
#include <ql/time/calendars/target.hpp>
#include <ql/utilities/dataformatters.hpp>

#include <iostream>
#include <iomanip>


BOOST_AUTO_TEST_CASE(esl_test_quantlib)
{
    using namespace QuantLib;
    // set up dates
    Calendar calendar = TARGET();
    Date todaysDate(15, May, 1998);
    Date settlementDate(17, May, 1998);
    //Settings::instance().evaluationDate() = todaysDate;

    // our options
    Option::Type type(Option::Put);
    Real underlying = 36;
    Real strike = 40;
    Spread dividendYield = 0.00;
    Rate riskFreeRate = 0.06;
    Volatility volatility = 0.20;
    Date maturity(17, May, 1999);
    DayCounter dayCounter = Actual365Fixed();

    std::cout << "Option type = " << type << std::endl;
    std::cout << "Maturity = " << maturity << std::endl;
    std::cout << "Underlying price = " << underlying << std::endl;
    std::cout << "Strike = " << strike << std::endl;
    std::cout << "Risk-free interest rate = " << io::rate(riskFreeRate)
        << std::endl;
    std::cout << "Dividend yield = " << io::rate(dividendYield)
        << std::endl;
    std::cout << "Volatility = " << io::volatility(volatility)
        << std::endl;
    std::cout << std::endl;
    std::string method;
    std::cout << std::endl;


    BOOST_TEST(true);
}

