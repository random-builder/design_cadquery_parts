#!/usr/bin/env bash

#
# perform conda package release
# 

export PACKAGE_VERSION=0.0.0
export PYTHON_VERSION=3.7

base_dir=$( cd $( dirname "$0" )/.. && pwd )
cd $base_dir
pwd

conda_base=$(conda info --base)
conda_build="$conda_base/conda-bld"

# remove all local packages
conda build purge-all

# build project artifacts
conda build tool/recipe-bundle \
    -c conda-forge \
    -c cadquery \

# upload project atrifacts
echo "### build: $conda_build"
find $conda_build -name *.tar.bz2 | while read file ; do
    echo "### upload: $file"
    anaconda upload --force --user random-builder $file
done
