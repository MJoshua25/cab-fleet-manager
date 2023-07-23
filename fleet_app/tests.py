import unittest
from django.test import Client


class FleetCarTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get("/fleet/carGestion")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
