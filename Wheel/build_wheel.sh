#!/bin/bash

virtualenv /tmp/build_pydbc_wheel_venv
source /tmp/build_pydbc_wheel_venv/bin/activate
pip install wheel

python setup.py bdist_wheel --dist-dir @CMAKE_INSTALL_PREFIX@/dist

deactivate
rm -r /tmp/build_pydbc_wheel_venv