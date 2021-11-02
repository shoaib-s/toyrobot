#!/usr/bin/env python3
# To use:
#       sudo python3 setup.py install
#

from setuptools import find_packages, setup

setup(
    name='toyrobot',
    version='1.0.0',
    maintainer='Shoaib',
    maintainer_email='shoaib.shaikh.pune@gmail.com',
    description='Toy Robot',
    packages=["rtoyrobo"],
    # include_package_data=True,
    # zip_safe=False,
    install_requires=[
        'pytest',
    ],
    entry_points={
        "console_scripts": [
            "toyrobot = toyrobot.__main__:main"
        ]
    }
)