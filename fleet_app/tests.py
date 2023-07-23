import unittest
from django.test import Client


class CarGestionTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get("/fleet/carGestion")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


class DriverGestionTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get("/fleet/driverGestion")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


class ContratGestionTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get("/fleet/contratGestion")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
