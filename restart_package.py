"""restart package

This script allows the user to uninstall weapon_detection package,
remove dist, build and weapon_detection.egg-info folders and
re-install the package.

Usage:
    python restart_package.py

Author:
    Ahmed Haj Yahme (hajyahmedahmed@gmail.com)
"""
import os
import shutil
os.system('pip uninstall weapon_detection')
shutil.rmtree('./dist', ignore_errors=True)
shutil.rmtree('./build', ignore_errors=True)
shutil.rmtree('./weapon_detection.egg-info', ignore_errors=True)
os.system('python setup.py sdist bdist_wheel')
os.system('pip install dist/weapon_detection-0.1-py3-none-any.whl')
