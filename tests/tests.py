#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

os.environ["MUNICIPALITY_NUMBER"] = "123123"
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

import unittest
from api_test import *

if __name__ == "__main__":
    unittest.main()

