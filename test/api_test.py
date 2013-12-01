#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import unittest
import json

import app

@unittest.skipUnless(os.environ.get("MATRIKKEL_USERNAME", None), "matrikkel username not set")
@unittest.skipUnless(os.environ.get("MATRIKKEL_PASSWORD", None), "matrikkel password not set")
class MatrikkelApiTest(unittest.TestCase):

    def setUp(self):
        self.app = app.create_app()

        self.client = self.app.test_client()

    def test_search_for_address(self):
        rv = self.client.get("/api/v1/addresses?query=ravelsveita")
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "Ravelsveita 4")

    def test_get_points_for_bnr_gnr(self):
        rv = self.client.get("/api/v1/buildings?gnr=402&bnr=188")
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["position"]["lat"], 63.43152178572586)
        self.assertEqual(data[0]["position"]["lon"], 10.39263181301638)
