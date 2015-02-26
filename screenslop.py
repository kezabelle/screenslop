#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
try:
    from urllib.parse import urlparse
except ImportError:  # Python 2
    from urlparse import urlparse
import sys
from PIL import Image
try:
    from http.client import CannotSendRequest
except ImportError: # Python 2
    from httplib import CannotSendRequest
from collections import namedtuple
from datetime import datetime
from itertools import product
from selenium import webdriver


__version_info__ = '0.1.0'
__version__ = '0.1.0'
version = '0.1.0'
def get_version():
    return version  # noqa


LANDSCAPE_RESOLUTIONS = (
        #(1920, 1080),
        #(1920, 1200), # Amazon Kindle Fire (HDX7)
        (1440, 900), # Generic notebook (HiDPI)
        (1366, 768),
        (1280, 800), # Google Nexus 10, Samsung Galaxy Tab 7.7/8.9/10.1
        (1024, 768),
        (1024, 600), # Amazon Kindle Fire (fist gen), Samsung Galaxy Tab
        (960, 600), # Google Nexus 7 2 (2013)
        (966, 604), # Google Nexus 7 (2012)
        (736, 414), # Apple iPhone 6plus
        (667, 375), # Apple iPhone 6
        (640, 400), # Samsung Galaxy Note
        (640, 384), # Google Nexus 4
        (640, 360), # Google Nexus 5, Samsung Galaxy Note 2/3, Samsung Galaxy S3/SNexus, S4
        (568, 320), # Apple iPhone 5
        (533, 320), # Google Nexus S, Samsung Galaxy S, S2,
        (480, 320), # Apple iPhone 3GS
)

PORTRAIT_RESOLUTIONS = tuple(
    (resolution[1], resolution[0])
    for resolution in LANDSCAPE_RESOLUTIONS
)

DEFAULT_RESOLUTIONS = LANDSCAPE_RESOLUTIONS + PORTRAIT_RESOLUTIONS


class Task(namedtuple('Task', 'window_size url')):
    @classmethod
    def from_string(cls, wxh):
        """
        Creates a new Task by parsing the NNNxNNN resolution.
        Does not include a `url` - use instance._replace to add one.
        """
        width, x, height = wxh.partition('x')
        return cls((width, height), None)
        
    @property
    def dimensions(self):
        return '{width!s}x{height!s}'.format(width=self.window_size[0],
                height=self.window_size[1])

    @property
    def width(self):
        return self.window_size[0]

    @property
    def height(self):
        return self.window_size[1]

    @property
    def is_portrait(self):
        return self.window_size[1] > self.window_size[0]

    @property
    def is_landscape(self):
        return not self.is_portrait

    @property
    def orientation(self):
        if self.is_portrait:
            return 'portrait'
        else:
            return 'landscape'


class Screenslop(object):
    __slots__ = ('window_sizes', 'urls', 'filename_template')

    def __init__(self, window_sizes, urls, filename_template='{orientation!s}_{window_size!s}.png'):
        self.window_sizes = window_sizes
        self.urls = urls
        self.filename_template = filename_template

    def get_tasks(self):
        data = product(self.window_sizes, self.urls)
        return (Task(window_size=window_size, url=url)
                for window_size, url in data)

    def get_filename_context(self, task):
        now = datetime.utcnow()
        filename_context = {
            'window_size': task.dimensions,
            'width': task.width,
            'height': task.height,
            'url': task.url,
            'parsed_url': urlparse(task.url),
            'now': now,
            'timetuple': now.utctimetuple(),
            'today': now.date(),
            'orientation': task.orientation,
        }
        return filename_context

    def get_screenshot_filename(self, task):
        filename_context = self.get_filename_context(task=task)
        return self.filename_template.format(**filename_context)

    def do_task(self, browser, task, callbacks=()):
        browser.set_window_size(*task.window_size)
        if browser.current_url != task.url:
            print("Fetching {url!s}".format(url=task.url), file=sys.stdout)
            browser.get(task.url)
        print("Doing viewport {dimensions!s}".format(dimensions=task.dimensions),
              file=sys.stdout)
        if len(callbacks) > 0:
            scripts_to_execute = (callback(task) for callback in callbacks)
            script_attempts = tuple(browser.execute_script(script)
                                    for script in scripts_to_execute)
        filename = self.get_screenshot_filename(task=task)
        browser.get_screenshot_as_file(filename)
        image = Image.open(filename)
        cropped_image = image.crop((0, 0, task.width, task.height))
        cropped_image.save('cropped_{filename!s}'.format(filename=filename))
        return None

    def get_browser(self):
        return webdriver.Firefox()


    def __call__(self, callbacks=(), filename_template=None):
        # allow override on a per-call basis.
        old_filename = self.filename_template
        if filename_template is not None:
            self.filename_template = filename_template

        browser = self.get_browser()
        try:
            results = tuple(self.do_task(browser=browser, task=task, callbacks=callbacks)
                            for task in self.get_tasks())
        finally:
            try:
                browser.quit()
            except CannotSendRequest as e:
                pass
        # hopefully restore the __init__ filename template
        self.filename_template = old_filename
        return results


def remove_debug_toolbar_if_exists(task):
    # Remove django-debug-toolbar if it exists, without polluting
    # the javascript namespace afterwards.
    return  """
    ;(function(document) {
        var djdebug_exists = document.getElementById('djDebug');
        if (djdebug_exists === void(0) || djdebug_exists === null) {
            return false;
        } else {
            djdebug_exists.remove();
            return true;
        }
    })(document);
    """



def run_via_cmd_line():
    try:
        if len(sys.argv) != 2:
            print("I only take a URL as an argument", file=sys.stderr)
            sys.exit(1)
        print("You can kill me with good ole' KeyboardInterrupt", file=sys.stdout)
        screenshotter = Screenslop(
            window_sizes=sorted(DEFAULT_RESOLUTIONS),
            urls=(sys.argv[1],)
        )
        output = screenshotter(
            callbacks=(remove_debug_toolbar_if_exists,)
        )
        if len(output) < 1:
            print("Something may've gone wrong", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)
    except KeyboardInterrupt as e:
        print("Killed by CTRL-C", file=sys.stdout)
        sys.exit(0)

if __name__ == '__main__':
    run_via_cmd_line()
