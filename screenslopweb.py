#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
import multiprocessing
from os import environ
from os import urandom
from django.utils.six import iteritems
from django.conf import settings
from screenslop import LANDSCAPE_RESOLUTIONS

__all__ = ['GunicornHandler']

DEBUG = environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = environ.get('SECRET_KEY', urandom(32))
ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS', 'localhost').split(',')
AVAILABLE_RESOLUTIONS = tuple(
    ('{0!s}x{1!s}'.format(*x),
     '{0!s}x{1!s}'.format(*x))
    for x in LANDSCAPE_RESOLUTIONS
)

settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
)

from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.template import Template
from django.template import Context
from django.forms import Form
from django.forms.fields import URLField
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.fields import MultipleChoiceField

class ScreenslopForm(Form):
    url = URLField()
    viewports = MultipleChoiceField(choices=AVAILABLE_RESOLUTIONS,
                                    widget=CheckboxSelectMultiple)


def index(request):
    form = ScreenslopForm(data=request.GET or None, files=None)
    template = Template("""
    {{ form.as_p }}
    """)
    context = Context({
        'form': form,
    })
    return HttpResponse(template.render(context))


urlpatterns = (
    url(r'^$', index),
)


from gunicorn.app.base import Application

class GunicornHandler(Application):
    def load_config(self):
        kwargs =  {
            'bind': '127.0.0.1:8080',
            'workers': multiprocessing.cpu_count(),
        }
        for key, value in iteritems(kwargs):
            self.cfg.set(key, value)

    def load(self):
        return get_wsgi_application()

application = GunicornHandler()
application.run()

