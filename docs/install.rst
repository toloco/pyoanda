.. _install:
==================
Installing pyoanda
==================

Pyoanda is on the Python Package Index (PyPI), so it can be installed standard Python tools like ``pip`` or ``easy_install``, and as well you can install from sources


Pypi
----

For an easy and always standard setup:

.. code-block:: bash

    $ pip install pyoanda



Manual
------
For a custom or developer installation:

.. code-block:: bash

    $ git clone git@github.com:toloco/pyoanda.git
    $ cd pyoanda
    $ python setup.py install
    # Make sure it works
    $ python setup.py test
