#!/usr/bin/python
# -*- coding: utf-8 -*-

from suds.client import Client
import xml.etree.ElementTree as ET
import suds
import os

import logging
import httplib, ssl, urllib2, socket
import base64

logging.basicConfig(level=logging.INFO)


class HTTPSConnectionV3(httplib.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)

    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        try:
            self.sock = ssl.wrap_socket(
                sock, self.key_file,
                self.cert_file,
                ssl_version=ssl.PROTOCOL_SSLv3
            )
        except ssl.SSLError, e:
            print("Trying SSLv23.")
            self.sock = ssl.wrap_socket(
                sock,
                self.key_file,
                self.cert_file,
                ssl_version=ssl.PROTOCOL_SSLv23
            )

class HTTPSHandlerV3(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSConnectionV3, req)


class MatrikkelService(object):

    def __init__(self, url, wsdl_url, username, password):
        self.url = url
        self.wsdl_url= wsdl_url

        self.username = username
        self.password = password

        # install opener
        opener = urllib2.build_opener(HTTPSHandlerV3())
        self.transport = suds.transport.https.HttpAuthenticated(
            username=username,
            password=password
        )
        self.transport.urlopener = opener
        self.client = self.create_client()

    def create_client(self):
        base64string = base64.encodestring(
            '%s:%s' % (self.username, self.password)
        ).replace('\n', '')

        authentication_header = {
            "WWW-Authenticate": "https://www.test.matrikkel.no",
            "Authorization" : "Basic %s" % base64string
        }

        client = Client(
            url=self.wsdl_url,
            location=self.url,
            transport = self.transport,
            username=self.username,
            password=self.password
        )
        client.set_options(headers=authentication_header)
        return client

def serialize_ident(ident):
    dict=  {
        "kommunenr": str(ident.kommunenr),
        "gardsnr": ident.gardsnr,
        "bruksnr": ident.bruksnr
    }
    try:
        dict["festenr"] =  ident.festenr
    except AttributeError:
        pass

    try:
        dict["seksjonsnr"] =  ident.seksjonsnr
    except AttributeError:
        pass

    return dict

class MatrikkelAdressService(MatrikkelService):

    def search_address(self, query, municipality_number):
        matrikkel_context = self.client.factory.create('ns2:MatrikkelContext')

        adresses =  self.client.service.findAdresserForVeg(
            query,
            municipality_number,
            matrikkel_context
        )

        result = []
        for address in adresses:

            address_ident = address.vegadresseIdent
            address_response = {
                "name": "%s %s" % (address.adressenavn, address_ident.nr)
            }
            try:
                address_response["name"] += address_ident.bokstav
            except AttributeError:
                pass

            try:
                address_response["matrikkel_ident"] = serialize_ident(
                    address.matrikkelenhetIdent
                )
                result.append(address_response)
            except AttributeError:
                pass
        return result


def create_point_dict(point):
        coord_string = point.point.coordinates.value.split(" ")
        return {
            "lon":float(coord_string[0]),
            "lat": float(coord_string[1])
            }

class MatrikkelBuildingService(MatrikkelService):

    def find_buildings(self,
                       kommunenr,
                       gardsnr,
                       bruksnr,
                       festenr=None,
                       seksjonsnr=None):


        matrikkelenhetident = self.client.factory.create('ns5:MatrikkelenhetIdent')
        matrikkelenhetident.kommunenr = kommunenr
        matrikkelenhetident.gardsnr = gardsnr
        matrikkelenhetident.bruksnr = bruksnr
        matrikkelenhetident.festenr = festenr
        matrikkelenhetident.seksjonsnr = seksjonsnr

        matrikkel_context = self.client.factory.create('ns2:MatrikkelContext')

        #EPSG:4326
        matrikkel_context.sosiKode = 84

        buildings = self.client.service.findBygningerForMatrikkelenhet(
            matrikkelenhetident,
            matrikkel_context
        )

        return [
            {"position": create_point_dict(building.representasjonspunkt)}
        for building in buildings
        ]