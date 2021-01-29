from conans import ConanFile, CMake, tools


class TrantorConan(ConanFile):
    name = "trantor"
    version = "1.2.0"
    license = "BSD"
    author = "an-tao"
    url = "https://github.com/an-tao/trantor"
    description = "a non-blocking I/O tcp network lib based on c++14/17"
    topics = ("trantor", "tcp-server", "linux", "non-blocking-io", "asynchronous-programming")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake", "cmake_find_package", "cmake_paths"
    requires = ["openssl/1.1.1i", "c-ares/1.17.1"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run("git clone https://github.com/an-tao/trantor")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("trantor/CMakeLists.txt", "project(trantor)",
                              '''project(trantor)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR} ${CMAKE_MODULE_PATH})''')

        if self.options.shared:
            tools.replace_in_file("trantor/CMakeLists.txt", "project(trantor)", 
                '''project(trantor)
set(BUILD_TRANTOR_SHARED true)''')
            self.run("echo 'shared true !'")
        else:
            self.run("echo 'shared false !'")
            pass

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="trantor")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/trantor %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="trantor")
        self.copy("*trantor.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="bin", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["trantor"]

