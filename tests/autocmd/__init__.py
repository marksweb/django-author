#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
short module explanation


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)

Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
from django.conf import settings
from django.db import models


try:
    from django.contrib.auth.management import create_superuser
except ImportError:
    def create_superuser(*args, **kwargs):
        pass

try:
    from django.db.models.signals import post_migrate
except ImportError:
    from django.db.models.signals import post_syncdb as post_migrate
# from django.contrib.auth import models as auth_models

settings.AUTO_CREATE_USER = getattr(settings, 'AUTO_CREATE_USER', True)

if settings.DEBUG and settings.AUTO_CREATE_USER:
    # From http://stackoverflow.com/questions/1466827/ --
    #
    # Prevent interactive question about wanting a superuser created. (This code
    # has to go in this otherwise empty "models" module so that it gets processed by
    # the "syncdb" command during database creation.)
    #
    # Create our own test user automatically.
    def create_testuser(app, created_models, verbosity, **kwargs):
        USERNAME = getattr(settings, 'QWERT_AUTO_CREATE_USERNAME', 'admin')
        PASSWORD = getattr(settings, 'QWERT_AUTO_CREATE_PASSWORD', 'admin')
        EMAIL = getattr(settings, 'QWERT_AUTO_CREATE_EMAIL', 'x@x.com')

        if getattr(settings, 'QWERT_AUTO_CREATE_USER', None):
            User = models.get_model(*settings.QWERT_AUTO_CREATE_USER.rsplit('.', 1))
        else:
            from django.contrib.auth.models import User

        try:
            User.objects.get(username=USERNAME)
        except User.DoesNotExist:
            if verbosity > 0:
                print('*' * 80)
                print('Creating test user -- login: %s, password: %s' % (USERNAME, PASSWORD))
                print('*' * 80)
            assert User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        else:
            if verbosity > 0:
                print('Test user already exists. -- login: %s, password: %s' % (USERNAME, PASSWORD))
    post_migrate.disconnect(
        create_superuser,
        sender="django.contrib.auth.models",
        dispatch_uid='django.contrib.auth.management.create_superuser',
    )
    post_migrate.connect(
        create_testuser,
        sender="django.contrib.auth.models",
        dispatch_uid='common.models.create_testuser',
    )
