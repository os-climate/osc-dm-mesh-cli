#!/bin/bash

#####
#
# environment.sh - Setup common environment variables
#
# Author: Eric Broda, eric.broda@brodagroupsoftware.com, August 17, 2023
#
# Parameters:
#   N/A
#
#####

if [ -z ${HOME_DIR+x} ] ; then
    echo "HOME_DIR environment variable has not been set (should be setup in your profile)"
    exit 1
fi

export ROOT_DIR="$HOME_DIR"
export PROJECT="bgs-dm-mesh-cli"
export PROJECT_DIR="$ROOT_DIR/$PROJECT"

export SAMPLES_DIR="$ROOT_DIR/bgs-dm-samples-dat"

$PROJECT_DIR/bin/show.sh