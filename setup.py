#!/usr/bin/env python

from setuptools import setup, find_packages
import subprocess

setup(name="singer-python",
      version='6.0.1',
      description="Singer.io utility library",
      author="Stitch",
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      url="http://singer.io",
      install_requires=[
          'pytz>=2018.4',
          'jsonschema==2.6.0',
          'simplejson==3.*',
          'python-dateutil>=2.6.0',
          'backoff==2.*',
          'ciso8601',
      ],
      extras_require={
          'dev': [
              'pylint',
              'ipython',
              'ipdb',
              'nose',
              'singer-tools'
          ]
      },
      packages=find_packages(),
      package_data = {
          'singer': [
              'logging.conf'
              ]
          },
)
