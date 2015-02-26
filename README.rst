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

This might work in a headless environment using ``xvfb`` or whatever.

Installation
------------

Currently, via ``git`` & ``pip``::

    pip install git+pip install git+https://github.com/kezabelle/screenslop.git
    
Or::

    pip install https://github.com/kezabelle/screenslop/archive/master.zip
    
Both of which should work under Python 2.7 & Python 3.3+. It may work elsewhere, I don't know.

Usage
-----

from the command line:: 

    $ screenslop http://localhost/
    
or if you prefer::

    $ /path/to/screenslop.py http://localhost/

Using either of the command line variants will hit the given URL for a number of 
common screen resolutions from 320 upwards, covering mobile and desktop dimensions.
Every resolution is captured in both portrait and landscape orientation by flipping
the width and height.

Alternatively, if you want to customise things, such a the dimensions tested, you
can drive the whole thing via python::

    from screenslop import Screenslop

    screenshot_instance = Screenslop(window_sizes=((1024, 768), (320, 480)),
                                     urls=('http://localhost/', 'https://example.com/'))
    screenshot_instance()

every ``url`` is hit once for every requested pair of dimensions; if the ``url``
hasn’t changed since the previous iteration, the page is **not reloaded**.

Screenshots
~~~~~~~~~~~

Every iteration should yield two screenshots to disk, one which
represents the full page, and one which just represents the viewport at a given
set of dimensions. The latter is always prefixed with ``cropped_...``

.. _selenium-controlled: http://www.seleniumhq.org/
.. _Firefox: https://www.mozilla.org/en-US/firefox/new/
