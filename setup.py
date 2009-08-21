from setuptools import setup, find_packages
import sys, os

version = '0.1.3'

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.txt')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

setup(name='basketweaver',
      version=version,
      description="Provides utilities for making your own python package index.",
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        ],
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
