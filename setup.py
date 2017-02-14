#!/usr/bin/env python

from setuptools import setup, find_packages
import subprocess


setup(name="singer-python",
      version="0.1.0",
      description="Singer.io utility library",
      author="Stitch",
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      url="http://singer.io",
      packages=find_packages(),
      package_data = {
          'singer': [
              'logging.conf'
              ]
          }
)
