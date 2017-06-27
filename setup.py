#!/usr/bin/env python

from setuptools import setup, find_packages
import subprocess

setup(name="singer-python",
      version='1.9.2',
      description="Singer.io utility library",
      author="Stitch",
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      url="http://singer.io",
      install_requires=[
          'pendulum==1.2.0',
          'simplejson==3.11.1',
      ],
      packages=find_packages(),
      package_data = {
          'singer': [
              'logging.conf'
              ]
          },
)
