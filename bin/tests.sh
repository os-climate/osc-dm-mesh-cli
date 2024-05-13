#!/bin/bash

#####
#
# tests.sh - Run test cases
#
# Runs pytest (which must be installed: "pip install pytest")
# and prints:
# - a short summary report (-ra)
# - with quiet mode(-q) (ie. minimal garbage output)
# - with non traceback info (--tb=no)
#
# NOTE: if you want to show logging statements you will
# need to add a flag "-s" to show them
#
# Author: Eric Broda, eric.broda@brodagroupsoftware.com, April 12, 2024
#
#####

pytest --tb=no -q -ra