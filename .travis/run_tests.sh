#!/bin/bash -xe
. /edx/app/programs/venvs/programs/bin/activate
cd /edx/app/programs/programs
pip install -U pip wheel
make requirements
make validate_translations
make validate
