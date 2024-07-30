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
        "use_globals": [True, False],
        "multiple_OD": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "single_thread": True,
        "config_debug": False,
        "use_globals": False,
        "multiple_OD": False,
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
