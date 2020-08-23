import json
import logging

import pytest
from werkzeug.wrappers import Response

from app.api import __version__

# from . import common

# VRP_DATA = common.VRP_DATA


class TestApp:
    @pytest.fixture()
    def test_data(self, origin, demand):
        # TODO: abstract json def
        origin_lat = origin["latitude"]
        origin_lon = origin["longitude"]

        return {
            "origin": {"latitude": origin_lat, "longitude": origin_lon},
            "unit": "pallets",
            "demand": demand,
            "vehicle_capacity": 26,
            "vehicle_definitions": None,  # TODO
        }

    @pytest.mark.parametrize(
        "content_type",
        [
            "audio/aac",
            "application/x-abiword",
            "application/x-freearc",
            "video/x-msvideo",
            "application/vnd.amazon.ebook",
            "application/octet-stream",
            "image/bmp",
            "application/x-bzip",
            "application/x-bzip2",
            "application/x-csh",
            "text/css",
            "text/csv",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.ms-fontobject",
            "application/epub+zip",
            "application/gzip",
            "image/gif",
            "text/html",
            "image/vnd.microsoft.icon",
            "text/calendar",
            "application/java-archive",
            "image/jpeg",
            "text/javascript, per the following specifications:",
            "audio/midi",
            "text/javascript",
            "audio/mpeg",
            "video/mpeg",
            "application/vnd.apple.installer+xml",
            "application/vnd.oasis.opendocument.presentation",
            "application/vnd.oasis.opendocument.spreadsheet",
            "application/vnd.oasis.opendocument.text",
            "audio/ogg",
            "video/ogg",
            "application/ogg",
            "audio/opus",
            "font/otf",
            "image/png",
            "application/pdf",
            "application/x-httpd-php",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "application/vnd.rar",
            "application/rtf",
            "application/x-sh",
            "image/svg+xml",
            "application/x-shockwave-flash",
            "application/x-tar",
            "image/tiff",
            "video/mp2t",
            "font/ttf",
            "text/plain",
            "application/vnd.visio",
            "audio/wav",
            "audio/webm",
            "video/webm",
            "image/webp",
            "font/woff",
            "font/woff2",
            "application/xhtml+xml",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/xml ",
            "application/vnd.mozilla.xul+xml",
            "application/zip",
            "video/3gpp",
            "video/3gpp2",
            "application/x-7z-compressed",
        ],
    )
    def test_non_json_request(self, client, content_type):
        """Test with content types other than 'application/json'"""

        logging.info(f"Testing with content-type : {content_type}")

        res: Response = client.post(
            f"/api/{__version__}/route", headers={"Content-Type": content_type}, data=""
        )

        logging.debug(f"Response : {res}")
        logging.debug(f"Response Data : {res.data}")

        assert res.status_code == 400
        assert res.headers["Content-Type"] == "application/json"
        assert (
            res.json["message"]
            == f"Incorrect request format! Content type received '{content_type}' instead of 'application/json'"
        )

    @pytest.mark.filterwarnings
    def test_main_procedure(self, client, test_data):
        """Test rpc with correct data"""
        logging.debug

        logging.debug(f"input data : {test_data}")

        endpoint = f"/api/{__version__}/route"
        logging.debug(f"endpoint: {endpoint}")

        # Send request
        response = client.post(endpoint, json=test_data)

        # Check if response is succesful
        assert response.status_code == 200
        # Check if response is of correct type
        assert response.is_json

        output = response.json

        assert len(output["solution"]) == len(test_data["demand"])
        assert output["origin"] == test_data["origin"]
        assert output["unit"] == test_data["unit"]
