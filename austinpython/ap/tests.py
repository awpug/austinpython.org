"""
Test home URLs.

"""
from django.test import TestCase
from django.test.client import Client

class HomePageTests(TestCase):
    """ A collection of tests ensuring the basic home pages are working. """

    def setUp(self):
        self.client = Client()

    def test_home(self):
        """ Test that home page works. """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
