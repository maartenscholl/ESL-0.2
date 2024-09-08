#define BOOST_TEST_MODULE est_test_version
#include <boost/test/unit_test.hpp>

#include <esl/version.hpp>


BOOST_AUTO_TEST_CASE(esl_test_version)
{
    auto v = esl::version();
    BOOST_TEST(true);
}

