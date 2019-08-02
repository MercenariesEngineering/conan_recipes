#!/bin/sh

conan user -p 94cb8468316779a44cdd6d3666d64fd3e4864cbc -r pierousseau pierousseau
#conan upload "*" -r pierousseau --all

conan upload Alembic/1.7.3@pierousseau/stable -r pierousseau --all
conan upload blosc/1.11.2@pierousseau/stable -r pierousseau --all
conan upload embree/3.5.2@pierousseau/stable -r pierousseau --all
conan upload freetype/2.9.1_with_Harfbuzz@pierousseau/stable -r pierousseau --all
conan upload fumefx/guerillaBinaries_4@pierousseau/stable -r pierousseau --all
conan upload glew/2.1.0@pierousseau/stable -r pierousseau --all
conan upload glfw/3.3@pierousseau/stable -r pierousseau --all
conan upload hdf5/1.10.1@pierousseau/stable -r pierousseau --all
conan upload jemalloc/4.3.1@pierousseau/stable -r pierousseau --all
conan upload libjpeg-turbo/1.5.2@pierousseau/stable -r pierousseau --all
conan upload llvm/3.5.1@pierousseau/stable -r pierousseau --all
conan upload nasm/2.13.01@pierousseau/stable -r pierousseau --all
conan upload OpenColorIO/1.1.1@pierousseau/stable -r pierousseau --all
conan upload OpenEXR/2.2.0@pierousseau/stable -r pierousseau --all
conan upload OpenExrId/1.0-beta.11@pierousseau/stable -r pierousseau --all
conan upload OpenImageDenoise/0.9.0@pierousseau/stable -r pierousseau --all
conan upload OpenImageIO/1.6.18@pierousseau/stable -r pierousseau --all
conan upload OpenVdb/4.0.2@pierousseau/stable -r pierousseau --all
conan upload partio/1.7.4@pierousseau/stable -r pierousseau --all
conan upload ptex/2.3.2@pierousseau/stable -r pierousseau --all
conan upload python/guerillaBinaries_2.6@pierousseau/stable -r pierousseau --all
conan upload re2/2019-06-01@pierousseau/stable -r pierousseau --all
conan upload TBB/2019_U6@pierousseau/stable -r pierousseau --all
conan upload USD/19.05@pierousseau/stable -r pierousseau --all
conan upload wxwidgets/2.8.12@pierousseau/stable -r pierousseau --all
