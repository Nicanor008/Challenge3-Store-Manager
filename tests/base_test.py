import unittest 
import json
from app import create_app

class BaseTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()