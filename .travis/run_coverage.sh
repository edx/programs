#!/bin/bash -xe
. /edx/app/programs/venvs/programs/bin/activate
cd /edx/app/programs/programs
coverage xml
