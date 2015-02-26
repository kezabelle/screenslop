Screenslop! (0.1.0)
===================

A quick and dirty way of testing responsive breakpoints for your CSS etc,
by smashing a `selenium-controlled`_ `Firefox`_ into a given ``url``
 at a number of resolutions.

Dependencies
------------

-  ``selenium``
-  ``PIL`` (well, ``Pillow`` really)
-  Firefox, obviously.

Usage
-----

from your python::

    from screenslop import Screenslop

    screenshot_instance = Screenslop(window_sizes=((1024, 768), (320, 480)),
                                     urls=('http://localhost/',))
    screenshot_instance()

from the command line::

    $ /path/to/screenslop.py http://localhost/

or, if ``setup.py`` worked ok::

    $ screenslop http://localhost/

every ``url`` is hit once for every requested pair of dimensions; if the ``url``
hasn’t changed since the previous iteration, the page is **not reloaded**.

Screenshots
~~~~~~~~~~~

Every iteration should yield two screenshots to disk, one which
represents the full page, and one which just represents the viewport at a given
set of dimensions. The latter is always prefixed with ``cropped_...``

.. _selenium-controlled: http://www.seleniumhq.org/
.. _Firefox: https://www.mozilla.org/en-US/firefox/new/
