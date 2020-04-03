#!/bin/sh

export CONAN_USER_HOME="C:/Conan_1/"
alias conan="/x/Tools/Python27/Scripts/conan.exe"

export lib=OpenExrId
export ver=1.0-beta.20

cd /x/Dev/ConanRecipes
rm -rf /c/Conan_1/.conan/data/${lib}/${ver}
conan export ${lib}_${ver}/conanfile.py ${lib}/${ver}@pierousseau/stable
#cd ../GuerillaConan/
#./build.sh

