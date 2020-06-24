#!/usr/bin/env python
from . import common
import logging

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class UserModelCase(unittest.TestCase):
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
    case = UserModelCase()
    case.setup()
    case.teardown()

def test_password_hashing():
    u = User(username='test')
    u.set_password('pass')
    assert not u.check_password('pas')
    assert u.check_password('pass')

