from setuptools import setup, find_packages
import os

version = '0.1.3'

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.txt')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

setup(name='basketweaver',
      version=version,
      description="Provides utilities for making your own python package " \
      "index plus a simple server for implementing pypi upload interface.",
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        ],
      keywords='python eggs pypi index package gz tar zip',
      author='Christopher Perkins, Chris McDonough',
      author_email='whit at myemma dot com',
      url='http://code.google.com/p/basket-weaver/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      distribution_links = ['http://github.com/whitmo/wee/tarball/master'],
      install_requires=[
          'gp.fileupload',
          'pastedeploy',
          'wee',
          #'pystache',
          'paste'
      ],
      
      entry_points="""
      [paste.app_factory]
      main = basketweaver.server:make_app

      [console_scripts]
      makeindex = basketweaver.makeindex:main
      """

   )
