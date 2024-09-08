cmake_minimum_required(VERSION 3.15)

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


find_package(Boost REQUIRED COMPONENTS unit_test_framework)

file(GLOB TEST_SOURCES "*.cpp")

foreach(TEST_SOURCE ${TEST_SOURCES})
    get_filename_component(TEST_NAME ${TEST_SOURCE} NAME_WE)
    add_executable(${TEST_NAME} ${TEST_SOURCE})
    target_link_libraries(${TEST_NAME} PRIVATE 
        esl 
        Boost::unit_test_framework
    )

    target_include_directories(${TEST_NAME} PRIVATE ${Boost_INCLUDE_DIRS})

    if(ESL_WITH_QUANTLIB)
        set(QUANTLIB_INCLUDE_DIR $ENV{QUANTLIB_INCLUDE_DIR})
        set(QUANTLIB_LIBRARY_DIR $ENV{QUANTLIB_LIBRARY_DIR})
        set(QUANTLIB_LIBRARY_NAME $ENV{QUANTLIB_LIBRARY_NAME})

        message(STATUS "QuantLib Include Dir: ${QUANTLIB_INCLUDE_DIR}")
        message(STATUS "QuantLib Library Dir: ${QUANTLIB_LIBRARY_DIR}")
        message(STATUS "QuantLib Library Name: ${QUANTLIB_LIBRARY_NAME}")
        
        target_compile_definitions(${TEST_NAME} PRIVATE QL_HIGH_RESOLUTION_DATE)
        target_include_directories(${TEST_NAME} PRIVATE ${QUANTLIB_INCLUDE_DIR})

        find_library(QUANTLIB_LIBRARY
            NAMES ${QUANTLIB_LIBRARY_NAME}
            PATHS ${QUANTLIB_LIBRARY_DIR}
            NO_DEFAULT_PATH
        )
        if(NOT QUANTLIB_LIBRARY)
            message(FATAL_ERROR "QuantLib library not found: ${QUANTLIB_LIBRARY_NAME}")
        endif()


        #target_link_libraries(${TEST_NAME} PRIVATE ${QUANTLIB_LIBRARY_DIR}/${QUANTLIB_LIBRARY_NAME})
        target_link_libraries(${TEST_NAME} PRIVATE ${QUANTLIB_LIBRARY})

    endif()

    add_test(NAME ${TEST_NAME} COMMAND ${TEST_NAME})

    # Diagnostics:
    #message(STATUS "Test name: ${TEST_NAME}")
    #get_target_property(TEST_INCLUDES ${TEST_NAME} INCLUDE_DIRECTORIES)
    #message(STATUS "${TEST_NAME} include directories: ${TEST_INCLUDES}")
endforeach()

set_tests_properties(${TEST_NAMES} PROPERTIES WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

