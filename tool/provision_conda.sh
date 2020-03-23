#!/usr/bin/env bash

#
# provision project environment
# 

base_dir=$( cd $( dirname "$0" )/.. && pwd )
cd $base_dir
pwd

eval "$(conda shell.bash hook)"

conda env remove -n cq_parts
conda env create -n cq_parts -f tool/cq_parts.env.yml
