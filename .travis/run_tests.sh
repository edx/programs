#!/bin/bash -xe
. /edx/app/programs/venvs/programs/bin/activate
cd /edx/app/programs/programs

pip install -U pip wheel

export DJANGO_SETTINGS_MODULE="programs.settings.test"

make requirements
make validate_translations
make static
make validate
