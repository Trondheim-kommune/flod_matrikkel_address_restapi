#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import unittest
import json
from base64 import b64encode

import app

@unittest.skipUnless(os.environ.get("MATRIKKEL_BASE_URL", None), "matrikkel url not set")
@unittest.skipUnless(os.environ.get("MATRIKKEL_USERNAME", None), "matrikkel username not set")
@unittest.skipUnless(os.environ.get("MATRIKKEL_PASSWORD", None), "matrikkel password not set")
class MatrikkelApiAddressTest(unittest.TestCase):

    def setUp(self):

        username = "test"
        password = "test"

        self.app = app.create_app(
            username,
            password,
            os.environ["MATRIKKEL_BASE_URL"],
            os.environ["MATRIKKEL_USERNAME"],
            os.environ["MATRIKKEL_PASSWORD"]
        )
        self.client = self.app.test_client()

        self.headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format(username, password))
        }

    def test_search_for_address(self):
        rv = self.client.get("/api/v1/addresses?query=ravelsveita", headers=self.headers)
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "Ravelsveita 4")

    def test_handle_special_chars(self):
        rv = self.client.get("/api/v1/addresses?query=kjøpmannsgata", headers=self.headers)
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)

        self.assertEqual(len(data), 54)
        self.assertEqual(data[0]["name"], u"Kjøpmannsgata 50")

    def test_handle_search_on_number(self):
        rv = self.client.get("/api/v1/addresses?query=kjøpmannsgata 50", headers=self.headers)
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], u"Kjøpmannsgata 50")

    def test_handle_search_on_number_and_letter(self):
        rv = self.client.get("/api/v1/addresses?query=kjøpmannsgata 16B", headers=self.headers)
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], u"Kjøpmannsgata 16B")

    def test_handle_search_on_number_and_letter_lowercase(self):
        rv = self.client.get("/api/v1/addresses?query=kjøpmannsgata 16b", headers=self.headers)
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], u"Kjøpmannsgata 16B")

    def test_handle_search_on_number_and_letter_with_space(self):
        rv = self.client.get("/api/v1/addresses?query=kjøpmannsgata 16 B", headers=self.headers)
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], u"Kjøpmannsgata 16B")

    def test_handle_search_on_number_and_letter_with_several_spaces(self):
        rv = self.client.get("/api/v1/addresses?query=kjøpmannsgata 16    B", headers=self.headers)
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], u"Kjøpmannsgata 16B")

@unittest.skipUnless(os.environ.get("MATRIKKEL_BASE_URL", None), "matrikkel url not set")
@unittest.skipUnless(os.environ.get("MATRIKKEL_USERNAME", None), "matrikkel username not set")
@unittest.skipUnless(os.environ.get("MATRIKKEL_PASSWORD", None), "matrikkel password not set")
class MatrikkelApiBuildingTest(unittest.TestCase):

    def setUp(self):
        username = "test"
        password = "test"

        self.app = app.create_app(
            username,
            password,
            os.environ["MATRIKKEL_BASE_URL"],
            os.environ["MATRIKKEL_USERNAME"],
            os.environ["MATRIKKEL_PASSWORD"]
        )
        self.client = self.app.test_client()

        self.headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format(username, password))
        }

    def test_get_points_for_bnr_gnr(self):
        rv = self.client.get("/api/v1/buildings?gardsnr=402&bruksnr=188", headers=self.headers)
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["position"]["lat"], 63.43152178572586)
        self.assertEqual(data[0]["position"]["lon"], 10.39263181301638)

    def test_should_not_return_bygningsendring(self):
        rv = self.client.get("/api/v1/buildings?gardsnr=16&bruksnr=60", headers=self.headers)
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(len(data), 17)

    def test_should_get_return_bygningsnummer(self):
        rv = self.client.get("/api/v1/buildings?gardsnr=402&bruksnr=188", headers=self.headers)
        self.assertEqual(200, rv.status_code)
        data = json.loads(rv.data)
        self.assertEqual(data[0]["building_number"], 182166081)