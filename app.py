#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from logging import StreamHandler
from flask import Flask

from api import create_api

API_VERSION = "v1"

def create_app():
    app = Flask(__name__)

    create_api(app, API_VERSION)
    if not app.debug:
        stream_handler = StreamHandler()
        app.logger.addHandler(stream_handler)

    return app


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5500))
    app = create_app()
    app.run(host='0.0.0.0', port=port, debug=True)
