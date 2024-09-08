from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import copy, get, chdir

import os

class ESLRecipe(ConanFile):
    name        = "esl"
    version     = "0.2.0"
    license     = "<Your License>"
    author      = "Maarten P. Scholl"
    url         = "https://github.com/INET-Complexity/ESL/"
    description = "Economic Simulation Library"
    
    topics   = ("esl", "simulation", "economics")
    settings = "os", "compiler", "build_type", "arch"
    
    options = {
        "shared":        [True, False],
        "fPIC":          [True, False],
        "with_python":   [True, False],
        "with_mpi":      [True, False],
        "build_tests":   [True, False],
        "with_quickfix": [True, False],
        "with_quantlib": [True, False],
        "with_osre":     [True, False]
    }
    default_options = {
        "shared":        False,
        "fPIC":          True,
        "with_python":   True,
        "with_mpi":      False,
        "build_tests":   True,
        "with_quickfix": False,
        "with_quantlib": True,
        "with_osre":     False
    }
    
    exports_sources = "CMakeLists.txt", "include/*", "src/*", "test/*", "python/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        self.options["boost"].shared       = False
        self.options["boost"].runtime_link = "static"
        self.options["boost"].runtime      = "static"

        self.options["quantlib"].shared       = False
        self.options["quantlib"].runtime_link = "static"
        self.options["quantlib"].runtime      = "static"
        
        self.settings.compiler.runtime     = "static"
        self.settings.compiler.runtime_type = "Release"

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        
        if self.settings.compiler == "msvc":
            tc.variables["CMAKE_MSVC_RUNTIME_LIBRARY"] = "MultiThreaded$<$<CONFIG:Debug>:Debug>"

        tc.variables["ESL_WITH_PYTHON"]   = self.options.with_python
        tc.variables["ESL_WITH_MPI"]      = self.options.with_mpi
        tc.variables["ESL_BUILD_TESTS"]   = self.options.build_tests
        tc.variables["ESL_WITH_QUICKFIX"] = self.options.with_quickfix
        tc.variables["ESL_WITH_QUANTLIB"] = self.options.with_quantlib
        tc.variables["ESL_WITH_OSRE"]     = self.options.with_osre
        
        if self.options.with_quantlib:
            quantlib = self.dependencies["quantlib"]
            tc.variables["QUANTLIB_INCLUDE_DIR"]  = quantlib.cpp_info.includedirs[0].replace("\\", "/")
            tc.variables["QUANTLIB_LIBRARY_DIR"]  = quantlib.cpp_info.libdirs[0].replace("\\", "/")
            tc.variables["QUANTLIB_LIBRARY_NAME"] = quantlib.cpp_info.libs[0].replace('.lib', '')

        tc.generate()

    def requirements(self):
        boost_options = { "without_python": True # not self.options.with_python
                        , "shared": False
                        , "multithreading": True
                        , 
                        }
        self.requires("boost/[>=1.85]", options=boost_options)
        
        self.requires("gsl/2.7")
        
        if self.options.with_quantlib:
            self.requires("quantlib/[>=1.35]")
            
        if self.options.with_mpi:
            self.requires("openmpi/4.1.0")

    def build_requirements(self):
        self.tool_requires("cmake/3.22.6")
        if self.options.with_quickfix:
            self.tool_requires("autoconf/2.71")
            self.tool_requires("libtool/2.4.7")

    def source(self):
        if self.options.with_osre:
            get(self, "https://github.com/OpenSourceRisk/Engine/archive/refs/heads/master.zip", strip_root=True, destination="osre")
            self.output.info(f"Open Source Risk Engine downloaded to {os.path.join(self.source_folder, 'osre')}")
        if self.options.with_quickfix:
            get(self, "https://github.com/quickfix/quickfix/archive/master.zip", strip_root=True, destination="quickfix")
            self.output.info(f"QuickFIX downloaded to {os.path.join(self.source_folder, 'quickfix')}")

    def build(self):
        self.source()
        if self.options.with_quickfix:
            quickfix_path = os.path.join(self.build_folder, "quickfix")
            self.output.info(f"QuickFIX path: {quickfix_path}")
            if not os.path.exists(quickfix_path):
                raise Exception(f"QuickFIX directory not found at {quickfix_path}")
            with chdir(self, quickfix_path):
                cmake = CMake(self)
                cmake.configure()
                cmake.build()

        if self.options.with_osre:
            osre_path = os.path.join(self.build_folder, "osre")
            cmake_osre = CMake(self)
            cmake_osre.configure(source_folder=osre_path)
            cmake_osre.build()
            cmake_osre.install()
        
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
                
        if self.options.build_tests:
            cmake.test(cli_args=["--verbose"])

    def package(self):
        cmake = CMake(self)
        cmake.install()

        if self.options.with_quickfix:
            quickfix_path = os.path.join(self.build_folder, "quickfix")
            copy(self, "*.h", src=os.path.join(quickfix_path, "include"), dst=os.path.join(self.package_folder, "include"))
            if self.settings.os == "Windows":
                copy(self, "*.lib", src=os.path.join(quickfix_path, "lib"), dst=os.path.join(self.package_folder, "lib"), keep_path=False)
                copy(self, "*.dll", src=os.path.join(quickfix_path, "lib"), dst=os.path.join(self.package_folder, "bin"), keep_path=False)
            else:
                copy(self, "*.so*", src=os.path.join(quickfix_path, "src", ".libs"), dst=os.path.join(self.package_folder, "lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["esl"]
        if self.options.with_python:
            self.cpp_info.defines.append("ESL_WITH_PYTHON")
        if self.options.with_mpi:
            self.cpp_info.defines.append("ESL_WITH_MPI")
        if self.options.with_quickfix:
            self.cpp_info.libs.append("quickfix")
        if self.options.with_quantlib:
            self.cpp_info.defines.append("ESL_WITH_QUANTLIB")
        if self.options.with_osre:
            self.cpp_info.libs.append("OREAnalytics")


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
