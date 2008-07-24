from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='basketweaver',
      version=version,
      description="Provides utilities for making your own python package index.",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='python eggs pypi index package gz tar zip',
      author='Christopher Perkins, Chris McDonough',
      author_email='chris@percious.com',
      url='http://code.google.com/p/basket-weaver/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          
      ],
      entry_points={
        'console_scripts': [
            'makeindex = basketweaver.makeindex:main'
            ],
        }
   )
