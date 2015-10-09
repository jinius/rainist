# -*- coding: utf-8 -*-
from os.path import abspath, dirname, join

SECRET_KEY = 'test secrect key'
DATABASE_SCHEMA = join(dirname(abspath(__file__)), 'schema.sql')

DOMAIN = 'http://localhost:5000'
FACEBOOK_APP_ID = '1667814513434441'
FACEBOOK_APP_SECRET = 'fd46a10d6904c688ea52601e0f11613f'
TWITTER_APP_ID = 'ddgfPhkIZ52w4uhxKjgk6EDQ0'
TWITTER_APP_SECRET = 'QjChmitIrr4rKIPY9ecVSQO3GPsuItmPv4NtqDHf4KVKnEwmGd'
