import unittest
import flask_testing

from flask import Flask
from flask_testing import TestCase


class TestNest3Levels(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):
        pass

    def test_test(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
