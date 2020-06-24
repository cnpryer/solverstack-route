#!/usr/bin/env python
from . import common
import logging

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class APIModelCase(unittest.TestCase):
    def setup(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

def test_app():
    case = APIModelCase()
    case.setup()
    case.teardown()