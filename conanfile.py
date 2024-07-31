from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.scm import Git


class CanopenlinuxRecipe(ConanFile):
    name = "canopenlinux"
    version = "4.0"
    package_type = "library"

    # Optional metadata
    license = "Apache-2.0"
    author = "<Put your name here> <And your email here>"
    url = "https://github.com/CANopenNode/CANopenLinux"
    description = " CANopenNode on Linux devices "
    topics = (
        "linux",
        "embedded",
        "realtime",
        "gateway",
        "canopen",
        "canopennode",
        "commander",
    )

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "single_thread": [True, False],
        "config_debug": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "single_thread": True,
        "config_debug": False,
    }

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "*.h", "*.c", "cocomm/*", "CANopenNode/*"

    def requirements(self):
        self.tool_requires("cmake/[>=3.23 <=3.30]")

    def validate(self):
        pass

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)

        # Setting to None will add the definition with no value
        tc.preprocessor_definitions["CO_MULTIPLE_OD"] = None
        # CO_USE_GLOBALS shouldn't define since CO_MULTIPLE_OD enabled.

        if self.options.single_thread:
            tc.preprocessor_definitions["CO_SINGLE_THREAD"] = None
        if self.options.config_debug:
            tc.preprocessor_definitions["CO_CONFIG_DEBUG"] = 0xFFFF

        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["canopenlinux"]
