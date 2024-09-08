cmake_minimum_required(VERSION 3.15)
project(esl VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)



if(MSVC)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
    add_compile_options(
        $<$<CONFIG:>:/MT> #---------|
        $<$<CONFIG:Debug>:/MTd> #---|-- Statically link the runtime libraries
        $<$<CONFIG:Release>:/MT> #--|
    )
    set(Boost_USE_STATIC_LIBS ON)
    set(Boost_USE_STATIC_RUNTIME ON)
endif()



find_package(Boost REQUIRED)

if(ESL_BUILD_TESTS)
    find_package(Boost REQUIRED COMPONENTS unit_test_framework)
endif()

find_package(GSL REQUIRED)

if(ESL_WITH_PYTHON)
    find_package(Python COMPONENTS Interpreter Development REQUIRED)
endif()

if(ESL_WITH_QUANTLIB)
    # Read QuantLib information from environment variables
    set(QUANTLIB_INCLUDE_DIR $ENV{QUANTLIB_INCLUDE_DIR})
    set(QUANTLIB_LIBRARY_DIR $ENV{QUANTLIB_LIBRARY_DIR})
    set(QUANTLIB_LIBRARY_NAME $ENV{QUANTLIB_LIBRARY_NAME})

    # Diagnostic output
    message(STATUS "QuantLib Include Dir: ${QUANTLIB_INCLUDE_DIR}")
    message(STATUS "QuantLib Library Dir: ${QUANTLIB_LIBRARY_DIR}")
    message(STATUS "QuantLib Library Name: ${QUANTLIB_LIBRARY_NAME}")

    # Check if variables are set
    if(NOT QUANTLIB_INCLUDE_DIR OR NOT QUANTLIB_LIBRARY_DIR OR NOT QUANTLIB_LIBRARY_NAME)
        message(FATAL_ERROR "QuantLib variables are not set correctly. Please check your Conan setup.")
    endif()

    # Create imported target for QuantLib
    add_library(QuantLib STATIC IMPORTED)
    set_target_properties(QuantLib PROPERTIES
        IMPORTED_LOCATION "${QUANTLIB_LIBRARY_DIR}/${QUANTLIB_LIBRARY_NAME}${CMAKE_STATIC_LIBRARY_SUFFIX}"
        INTERFACE_INCLUDE_DIRECTORIES "${QUANTLIB_INCLUDE_DIR}"
    )
endif()



if(ESL_WITH_QUANTLIB)
    message(STATUS "QuantLib Include Dir: ${QUANTLIB_INCLUDE_DIR}")
    message(STATUS "QuantLib Library Dir: ${QUANTLIB_LIBRARY_DIR}")
    message(STATUS "QuantLib Library Name: ${QUANTLIB_LIBRARY_NAME}")
endif()



add_library(esl src/esl.cpp)
target_include_directories(esl PUBLIC include)
target_link_libraries(esl PUBLIC Boost::boost GSL::gsl)

#if(ESL_WITH_QUANTLIB)
#    target_compile_definitions(esl PUBLIC QL_HIGH_RESOLUTION_DATE)
#    target_link_libraries(esl PUBLIC QuantLib::QuantLib)
#    # Add QuantLib include directories to ESL
#    get_target_property(QUANTLIB_INCLUDE_DIRS QuantLib::QuantLib INTERFACE_INCLUDE_DIRECTORIES)
#    target_include_directories(esl PUBLIC ${QUANTLIB_INCLUDE_DIRS})
#endif()
if(ESL_WITH_QUANTLIB)
    target_compile_definitions(esl PUBLIC QL_HIGH_RESOLUTION_DATE)
    target_link_libraries(esl PUBLIC QuantLib)
    target_include_directories(esl PUBLIC ${QUANTLIB_INCLUDE_DIR})
endif()


if(ESL_WITH_PYTHON)
    target_include_directories(esl PRIVATE ${Python_INCLUDE_DIRS})
    target_link_libraries(esl PRIVATE Python::Python)
    target_compile_definitions(esl PRIVATE ESL_WITH_PYTHON)
endif()

if(ESL_WITH_MPI)
    find_package(MPI REQUIRED)
    target_link_libraries(esl PUBLIC MPI::MPI_CXX)
    target_compile_definitions(esl PRIVATE ESL_WITH_MPI)
endif()


if(ESL_BUILD_TESTS)
    enable_testing()    
    add_subdirectory(test)
    
    include_directories(${Boost_INCLUDE_DIRS})
endif()

install(TARGETS esl
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib
        RUNTIME DESTINATION bin
        INCLUDES DESTINATION include)
install(DIRECTORY include/ DESTINATION include)
