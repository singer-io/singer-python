#!/usr/bin/env python

from setuptools import setup, find_packages
import subprocess

setup(name="singer-python",
      version='1.6.0a4',
      description="Singer.io utility library",
      author="Stitch",
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      url="http://singer.io",
      install_requires=[
          'pendulum==1.2.0',
      ],
      packages=find_packages(),
      package_data = {
          'singer': [
              'logging.conf'
              ]
          },
)
