#!/bin/sh

base_dir="$(conan config home)"
echo "Analysing recipes exported to $base_dir"

function CheckRecipe()
{
	local package=$1
	local name_version="$(echo $package | cut -d '@' -f1)"
	local repo_version="$(echo $package | cut -d '@' -f2)"
	local name="$(echo $name_version | cut -d '/' -f1)"
	local version="$(echo $name_version | cut -d '/' -f2)"
	local repo="$(echo $repo_version | cut -d '/' -f1)"
	local recipe_version="$(echo $repo_version | cut -d '/' -f2)"

	local git_file=${name}_${version}/conanfile.py
	local conan_file=$base_dir/data/$name/$version/$repo/$recipe_version/export/conanfile.py

	if [ -f $conan_file ]; then
		local has_diff="$(diff -wrq $git_file $conan_file )"
		if [ "$has_diff" ]; then
			echo "********"
			echo diff -w $git_file $conan_file
			echo 
			diff -w $git_file $conan_file
		else
			echo "$package is up to date"
		fi
	else
		echo " --- $package has not been exported"
	fi
}

CheckRecipe Alembic/1.7.12@mercseng/v1
CheckRecipe b2/4.2.0@mercseng/v0
CheckRecipe bison/3.5.3@mercseng/v0
CheckRecipe blosc/1.11.2@mercseng/v0
CheckRecipe boost/1.73.0@mercseng/v0
CheckRecipe bzip2/1.0.8@mercseng/v0
CheckRecipe catch2/3.0.0-preview3@mercseng/v0
CheckRecipe cmake/3.17.3@mercseng/v0
CheckRecipe cpython/3.7.7@mercseng/v0
CheckRecipe double-conversion/3.1.5@mercseng/v0
CheckRecipe eigen/3.3.7@mercseng/v0
CheckRecipe embree/3.9.0@mercseng/v1
CheckRecipe expat/2.2.9@mercseng/v0
CheckRecipe FBX/2020.0.1@mercseng/v0
CheckRecipe flex/2.6.4@mercseng/v0
CheckRecipe fontstash/1.0.1@mercseng/v0
CheckRecipe freetype/2.10.2_with_Harfbuzz@mercseng/v0
CheckRecipe fumefx/4.0@mercseng/v0
CheckRecipe gdbm/1.18.1@mercseng/v0
CheckRecipe glew/2.1.0@mercseng/v0
CheckRecipe glfw/3.3@mercseng/v0
CheckRecipe glu/9.0.1@mercseng/v0
CheckRecipe GSL/2.1.0@mercseng/v0
CheckRecipe hdf5/1.10.6@mercseng/v0
CheckRecipe icu/64.2@mercseng/v0
CheckRecipe ispc/1.13.0@mercseng/v0
CheckRecipe ispc/1.9.2@mercseng/v0
CheckRecipe jbig/20160605@mercseng/v0
CheckRecipe jemalloc/4.3.1@mercseng/v0
CheckRecipe jom_installer/1.1.2@mercseng/v0
CheckRecipe libalsa/1.2.2@mercseng/v0
CheckRecipe libcurl/7.71.0@mercseng/v0
CheckRecipe libffi/3.3@mercseng/v0
CheckRecipe libiconv/1.15@mercseng/v0
CheckRecipe libjpeg-turbo/1.5.2@mercseng/v0
CheckRecipe libpng/1.6.37@mercseng/v0
CheckRecipe libsndfile/1.0.29@mercseng/v0
CheckRecipe libtiff/4.0.9@mercseng/v0
CheckRecipe libunwind/1.3.1@mercseng/v0
CheckRecipe libuuid/1.0.3@mercseng/v0
CheckRecipe libwebp/1.1.0@mercseng/v0
CheckRecipe libxml2/2.9.9@mercseng/v0
CheckRecipe llvm/3.5.1@mercseng/v0
CheckRecipe lzma/5.2.4@mercseng/v0
CheckRecipe m4/1.4.18@mercseng/v0
CheckRecipe materialx/1.37.1@mercseng/v0
CheckRecipe nasm/2.13.02@mercseng/v0
CheckRecipe ncurses/6.2@mercseng/v0
CheckRecipe ninja/1.10.0@mercseng/v0
CheckRecipe OpenColorIO/1.1.1@mercseng/v0
CheckRecipe OpenEXR/2.5.1@mercseng/v0
CheckRecipe OpenExrId/1.0-beta.22@mercseng/v0
CheckRecipe OpenImageDenoise/1.0.0@mercseng/v1
CheckRecipe OpenImageIO/2.1.15.0@mercseng/v0
CheckRecipe OpenSSL/1.1.1g@mercseng/v0
CheckRecipe OpenSubdiv/3.4.3@mercseng/v0
CheckRecipe OpenVdb/6.2.1@mercseng/v0
CheckRecipe partio/1.7.4@mercseng/v0
CheckRecipe pcre2/10.33@mercseng/v0
CheckRecipe PortAudio/2018-12-24@mercseng/v0
CheckRecipe ptex/2.3.2@mercseng/v0
CheckRecipe pybind11/2.5.0@mercseng/v0
CheckRecipe PySide2/5.12.6@mercseng/v0
CheckRecipe python/2.6@mercseng/v0
CheckRecipe qt/5.12.6@mercseng/v0
CheckRecipe rapidjson/1.1.0@mercseng/v0
CheckRecipe re2/2019-06-01@mercseng/v0
CheckRecipe readline/8.0@mercseng/v0
CheckRecipe rumba-python/1.0.0@mercseng/v0
CheckRecipe rumba-python-dev/1.0.0@mercseng/v0
CheckRecipe spdlog-rumba/1.5.0@mercseng/v0
CheckRecipe sqlite3/3.32.3@mercseng/v0
CheckRecipe tbb/2020.02@mercseng/v1
CheckRecipe unistd/1.0@mercseng/v0
CheckRecipe USD/20.05@mercseng/v4
CheckRecipe USD/20.11@mercseng/v1
CheckRecipe winflexbison/2.5.22@mercseng/v0
CheckRecipe wxwidgets/2.8.12@mercseng/v0
CheckRecipe zlib/1.2.11@mercseng/v0
CheckRecipe zstd/1.4.5@mercseng/v0
