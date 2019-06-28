#!/bin/sh

conan user -p 94cb8468316779a44cdd6d3666d64fd3e4864cbc -r pierousseau pierousseau
#conan upload "*" -r pierousseau --all

conan upload Alembic/1.7.3@pierousseau/stable -r pierousseau --all
conan upload blosc/1.11.2@pierousseau/stable -r pierousseau --all
conan upload embree/guerillaBinaries_3.2.0@pierousseau/stable -r pierousseau --all
conan upload embree/3.5.2@pierousseau/stable -r pierousseau --all
conan upload fumefx/guerillaBinaries_4@pierousseau/stable -r pierousseau --all
#conan upload GuerillaBinaries/1.0@pierousseau/stable -r pierousseau --all
conan upload hdf5/1.10.1@pierousseau/stable -r pierousseau --all
conan upload jemalloc/4.3.1@pierousseau/stable -r pierousseau --all
conan upload libjpeg-turbo/1.5.2@pierousseau/stable -r pierousseau --all
conan upload llvm/guerillaBinaries_3.5.1@pierousseau/stable -r pierousseau --all
conan upload llvm/3.5.1@pierousseau/stable -r pierousseau --all
conan upload nasm/2.13.01@pierousseau/stable -r pierousseau --all
conan upload opencolorio/guerillaBinaries_1.0.8@pierousseau/stable -r pierousseau --all
conan upload OpenEXR/2.2.0@pierousseau/stable -r pierousseau --all
conan upload OpenExrId/1.0-beta.11@pierousseau/stable -r pierousseau --all
conan upload OpenImageDenoise/0.9.0@pierousseau/stable -r pierousseau --all
conan upload OpenImageIO/1.6.18@pierousseau/stable -r pierousseau --all
conan upload OpenVdb/4.0.2@pierousseau/stable -r pierousseau --all
conan upload partio/1.7.4@pierousseau/stable -r pierousseau --all
conan upload ptex/guerillaBinaries_2.0.30@pierousseau/stable -r pierousseau --all
conan upload python/guerillaBinaries_2.6@pierousseau/stable -r pierousseau --all
conan upload re2/2019-06-01@pierousseau/stable -r pierousseau --all
conan upload wx/guerillaBinaries_2.8.8@pierousseau/stable -r pierousseau --all
