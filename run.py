#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from app import create_app

username = os.environ["FLOD_MATRIKKEL_USER"]
password = os.environ["FLOD_MATRIKKEL_PASS"]

matrikkel_user = os.environ["MATRIKKEL_USERNAME"]
matrikkel_password = os.environ["MATRIKKEL_PASSWORD"]

application = create_app(username, password, matrikkel_user, matrikkel_password)