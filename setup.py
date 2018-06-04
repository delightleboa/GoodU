#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import glob
import subprocess
if False:
    from typing import Any, Dict, Optional

WYZEPAL_BOTS_VERSION = "0.4.7"
IS_PYPA_PACKAGE = False


package_data = {
    '': ['doc.md', '*.conf', 'assets/*']
}

# IS_PYPA_PACKAGE is set to True by tools/release-packages
# before making a PyPA release.
if not IS_PYPA_PACKAGE:
    package_data[''].append('fixtures/*.json')
    package_data[''].append('logo.*')

# We should be installable with either setuptools or distutils.
package_info = dict(
    name='wyzepal_bots',
    version=WYZEPAL_BOTS_VERSION,
    description='WyzePal\'s Bot framework',
    author='WyzePal Open Source Project',
    author_email='wyzepal-devel@googlegroups.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Communications :: Chat',
    ],
    url='https://www.wyzepal.org/',
    entry_points={
        'console_scripts': [
            'wyzepal-run-bot=wyzepal_bots.run:main',
            'wyzepal-terminal=wyzepal_bots.terminal:main'
        ],
    },
    include_package_data=True,
)  # type: Dict[str, Any]

setuptools_info = dict(
    install_requires=[
        'pip',
        'wyzepal',
    ],
)

try:
    from setuptools import setup, find_packages
    package_info.update(setuptools_info)
    package_info['packages'] = find_packages()
    package_info['package_data'] = package_data

except ImportError:
    from distutils.core import setup
    from distutils.version import LooseVersion
    from importlib import import_module

    # Manual dependency check
    def check_dependency_manually(module_name, version=None):
        # type: (str, Optional[str]) -> None
        try:
            module = import_module(module_name)  # type: Any
            if version is not None:
                assert(LooseVersion(module.__version__) >= LooseVersion(version))
        except (ImportError, AssertionError):
            if version is not None:
                print("{name}>={version} is not installed.".format(
                    name=module_name, version=version), file=sys.stderr)
            else:
                print("{name} is not installed.".format(name=module_name), file=sys.stderr)
            sys.exit(1)

    check_dependency_manually('wyzepal')
    check_dependency_manually('mock', '2.0.0')
    check_dependency_manually('html2text')
    check_dependency_manually('PyDictionary')

    # Include all submodules under bots/
    package_list = ['wyzepal_bots']
    dirs = os.listdir('wyzepal_bots/bots/')
    for dir_name in dirs:
        if os.path.isdir(os.path.join('wyzepal_bots/bots/', dir_name)):
            package_list.append('wyzepal_bots.bots.' + dir_name)
    package_info['packages'] = package_list

setup(**package_info)

# Install all requirements for all bots. get_bot_paths()
# has requirements that must be satisfied prior to calling
# it by setup().
current_dir = os.path.dirname(os.path.abspath(__file__))
bots_dir = os.path.join(current_dir, "wyzepal_bots", "bots")
bots_subdirs = map(lambda d: os.path.abspath(d), glob.glob(bots_dir + '/*'))
bot_paths = filter(lambda d: os.path.isdir(d), bots_subdirs)
for bot_path in bot_paths:
    req_path = os.path.join(bot_path, 'requirements.txt')
    if os.path.exists(req_path):
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', req_path, '--quiet'])
