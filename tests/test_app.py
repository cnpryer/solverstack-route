#!/usr/bin/env python
from . import common
import logging

from datetime import datetime, timedelta
import unittest
from app import create_app
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class APIModelCase(unittest.TestCase):
    def setup(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def teardown(self):
        pass

def test_app():
    case = APIModelCase()
    case.setup()
    case.teardown()