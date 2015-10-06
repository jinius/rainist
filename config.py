# -*- coding: utf-8 -*-
from os.path import abspath, dirname, join

SECRET_KEY = 'test secrect key'
DATABASE_SCHEMA = join(dirname(abspath(__file__)), 'schema.sql')
