# Configuration

## Profile file

For Windows, you need this ```~/.conan/prpfile/default``` profile file :
```
[build_requires]
[settings]
os=Windows
arch=x86_64
compiler=Visual Studio
compiler.version=14
build_type=Release
arch_build=x86_64
os_build=Windows
[options]
[env]
CONAN_CMAKE_GENERATOR="Visual Studio 14 2015 Win64"
```

Because of a conan bug, you may have to add the following variable to the environment:
```
CONAN_CMAKE_GENERATOR="Visual Studio 14 2015 Win64"
```

## Remove repository

Add the remote repository:
```
conan remote add rumba_libs https://api.bintray.com/conan/tdelame/rumba_libs --insert 0
```

To upload you will need to exec with SECRET_API_KEY:
```
conan user -p SECRET_API_KEY -r rumba_libs tdelame
```

# Build a library

## Build a lib in all required version

To build portaudio in all versions for your os :

```
cd conan_recipes
./conan_create portaudio_2018-12-24.py
```

## Upload the binaries

```
conan upload PortAudio/2018-12-24@tdelame/stable --all -r=rumba_libs
```

# Localy build a project

Let's build and fix localy libsndfile_1.0.28.

Download the source
```
conan source libsndfile_1.0.28.py --source-folder=tmp/source
```

Copy the source (to create a diff)
```
cp -r tmp/source tmp/source_orig
```

Generate the makefile
```
conan install libsndfile_1.0.28.py --install-folder=tmp/build
```

Build the library
```
conan build libsndfile_1.0.28.py --source-folder=tmp/source --build-folder=tmp/build
```

Package the library
```
conan package libsndfile_1.0.28.py --source-folder=tmp/source --build-folder=tmp/build --package-folder=tmp/package
```
