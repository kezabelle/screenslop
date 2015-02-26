#! /usr/bin/env python
from sys import exit
from datetime import datetime
from itertools import product
from selenium import webdriver

RESOLUTIONS = (
        (360, 480),
        (400, 600),
        (480, 320),
        (600, 400),
)

URLS = (
        'http://localhost:8080/',
)

if __name__ == '__main__':
    browser = webdriver.Firefox()
    remove_debug_toolbar_if_exists = """
    var djdebug_exists = document.getElementById('djDebug');
    if (djdebug_exists === void(0) || djdebug_exists === null) {}
    else {
        djdebug_exists.remove();
    }
    """

    try:
        for window_size, url in product(RESOLUTIONS, URLS):
            browser.set_window_size(*window_size)
            browser.get(url)
            browser.execute_script(remove_debug_toolbar_if_exists)
            wxh = '{0!s}x{1!s}'.format(*window_size)
            filename = '{dims!s}_{dt!s}.png'.format(dims=wxh,
                                                    dt=datetime.today())
            browser.get_screenshot_as_file(filename)
    finally:
        browser.quit()
    exit(0)