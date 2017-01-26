#!/usr/bin/env python

from setuptools import setup, find_packages
import subprocess


setup(name="stitchstream-python",
      version="0.4.1",
      description="Write the stitchstream format from Python",
      author="Stitch",
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      url="https://github.com/stitchdata/stitchstream-python",
      packages=find_packages(),
      package_data = {
          'stitchstream': [
              'logging.conf'
              ]
          }
)
