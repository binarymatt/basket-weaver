basketweaver
============

``basketweaver`` is a tool for creating your own package index out of a directory full
of eggs. You can then point to this index with e.g. ``zc.buildout`` or ``setuptools``
and thus be independant of PyPI.

Usage
-----

Here is a quick example on how to install and use it::

      easy_install basketweaver
      cd <a/directory/with/eggs/>
      makeindex *

This will create an ``index`` folder with links to all eggs.

You can then make point a webserver to this directory and use this link in your ``zc.buildout``
configuration or ``easy_install`` command.


Code
----

This project is hosted at http://code.google.com/p/basket-weaver/
