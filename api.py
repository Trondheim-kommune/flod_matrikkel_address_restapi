#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
from flask import request, Response, abort

from matrikkel import MatrikkelBuildingService, MatrikkelAdressService

MUNICIPALITY_NR = "1601"

def create_api(app, api_version):

    username = os.environ["MATRIKKEL_USERNAME"]
    password = os.environ["MATRIKKEL_PASSWORD"]

    address_service = MatrikkelAdressService(
        'https://www.test.matrikkel.no/innsynapi_v3/adresse/AdresseWebService?WSDL',
        'file://%s/AdresseWebService.xml' % (os.getcwd()),
        username,
        password
    )

    building_service = MatrikkelBuildingService(
        'https://www.test.matrikkel.no/innsynapi_v3/bygning/BygningWebService?WSDL',
        'file://%s/BygningWebService.xml' % (os.getcwd()),
        username,
        password
    )

    @app.route("/api/%s/addresses" % api_version)
    def addresses_api():
        query = request.args.get('query', None)
        if query:
            addresses = address_service.search_address(
                query.decode("UTF-8"), MUNICIPALITY_NR
            )
            return Response(json.dumps(addresses), mimetype="application/json")
        abort(404)

    @app.route("/api/%s/buildings" % api_version)
    def buildings_api():
        bnr = request.args.get('bnr', None)
        gnr = request.args.get('gnr', None)
        fnr = request.args.get('fnr', None)
        snr = request.args.get('snr', None)
        if bnr and gnr:
            buildings = building_service.find_buildings(
                MUNICIPALITY_NR,
                gnr,
                bnr,
                fnr,
                snr
            )
            return Response(json.dumps(buildings), mimetype="application/json")
        abort(404)