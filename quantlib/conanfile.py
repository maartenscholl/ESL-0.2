# This Conan File is distributed as part of the Economic Simulation Library and does not pretend to be an official QuantLib package 
# or even a recommended approach to installing QuantLib for your own projects.

from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import get, copy, chdir
import os

class QuantLibConan(ConanFile):
    name        = "quantlib"
    version     = "1.35"
    license     = "BSD-3-Clause"
    author      = "Luigi Ballabio"
    url         = "https://github.com/lballabio/QuantLib"
    description = "The QuantLib project (https://www.quantlib.org) is aimed at providing a comprehensive software framework for quantitative finance. QuantLib is a free/open-source library for modeling, trading, and risk management in real-life. QuantLib is Non-Copylefted Free Software and OSI Certified Open Source Software."
    topics      = ("quantitative-finance", "financial-instruments")
    settings    = "os", "compiler", "build_type", "arch"
    
    options     = { "shared":               [True, False]
                  , "fPIC":                 [True, False]
                  , "high_resolution_date": [True, False]  # Option to toggle QL_HIGH_RESOLUTION_DATE for intraday precision
                  }

    default_options = { "shared":               False
                      , "fPIC":                 True
                      , "high_resolution_date": False  # Default: QL_HIGH_RESOLUTION_DATE is disabled
                      }
    
    exports_sources = "CMakeLists.txt", "src/*", "include/*"   

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.settings.compiler == "msvc":
            self.options["boost"].shared       = False
            self.options["boost"].runtime_link = "static"
            self.settings.compiler.runtime     = "static"
    
    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)

        tc.variables["CMAKE_MSVC_RUNTIME_LIBRARY"] = "MultiThreaded$<$<CONFIG:Debug>:Debug>"

        if self.options.high_resolution_date:
            tc.cache_variables["QL_HIGH_RESOLUTION_DATE"] = "ON"
    
        tc.cache_variables["QL_BUILD_BENCHMARK"]    = "OFF"
        tc.cache_variables["QL_BUILD_EXAMPLES"]     = "OFF"
        tc.cache_variables["QL_BUILD_TEST_SUITE"]   = "OFF"
        tc.cache_variables["QL_INSTALL_BENCHMARK"]  = "OFF"
        tc.cache_variables["QL_INSTALL_EXAMPLES"]   = "OFF"
        tc.cache_variables["QL_INSTALL_TEST_SUITE"] = "OFF"
        tc.generate()

    def source(self):
        get(self, "https://github.com/lballabio/QuantLib/releases/download/v1.35/QuantLib-1.35.zip", destination='..', strip_root=True)

    def build(self):
        self.source()
        with chdir(self, self.build_folder):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()
            cmake.install()
        
    def build_requirements(self):
        self.tool_requires("cmake/3.22.6")

    def requirements(self):
        boost_options = { "without_python": True
                        , "shared": False
                        , "multithreading": True
                        }
        self.requires("boost/[>=1.85.0]", options=boost_options)

    def package(self):
        copy(self, "*.hpp", src=os.path.join(self.build_folder, "install", "include"), dst=os.path.join(self.package_folder, "include"))
        copy(self, "*.h",   src=os.path.join(self.build_folder, "install", "include"), dst=os.path.join(self.package_folder, "include"))

        copy(self, "*.lib", src=os.path.join(self.build_folder, "install", "lib"), dst=os.path.join(self.package_folder, "lib"))
        copy(self, "*.so*", src=os.path.join(self.build_folder, "install", "lib"), dst=os.path.join(self.package_folder, "lib"))

        copy(self, "*.dll", src=os.path.join(self.build_folder, "install", "bin"), dst=os.path.join(self.package_folder, "bin"))
        
        copy(self, "LICENSE.TXT", dst="licenses", src=self.source_folder)
        

    def package_info(self):
        lib_dir = os.path.join(self.package_folder, "lib")
        libs = [f for f in os.listdir(lib_dir) if f.startswith("QuantLib") and f.endswith(".lib")]
        if libs:
            self.cpp_info.libs = libs
        else:
            self.cpp_info.libs = ["QuantLib"]  # Fallback to default name

        self.cpp_info.set_property("cmake_target_name", "QuantLib::QuantLib")
        self.cpp_info.set_property("cmake_file_name", "QuantLib")
        self.cpp_info.set_property("pkg_config_name", "quantlib")
        self.cpp_info.set_property("license", "BSD-3-Clause")
        self.cpp_info.set_property("license_type", "BSD-3-Clause-Custom")
        self.cpp_info.includedirs = ["include"] #  [os.path.join("include", "ql")]
        self.cpp_info.libdirs = ["lib"]
        
        if self.settings.compiler == "msvc":
            if self.settings.build_type == "Debug":
                self.cpp_info.defines.append("_DEBUG")
            if self.settings.compiler.runtime == "static":
                self.cpp_info.defines.append("_MT")
            elif self.settings.compiler.runtime == "dynamic":
                self.cpp_info.defines.append("_MT")
                self.cpp_info.defines.append("_DLL")

        self.output.info(f"Compiler runtime: {self.settings.compiler.runtime}")
        self.output.info(f"Build type: {self.settings.build_type}")
        self.output.info(f"QuantLib library name: {self.cpp_info.libs[0]}")
