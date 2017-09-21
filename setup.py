#!/usr/bin/env python

from setuptools import setup, find_packages
import subprocess

setup(name="singer-python",
      version='3.3.0',
      description="Singer.io utility library",
      author="Stitch",
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      url="http://singer.io",
      install_requires=[
          'jsonschema==2.6.0',
          'pendulum==1.2.0',
          'simplejson==3.11.1',
          'python-dateutil==2.6.0',
      ],
      packages=find_packages(),
      package_data = {
          'singer': [
              'logging.conf'
              ]
          },
)
