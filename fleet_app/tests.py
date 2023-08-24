import unittest
from django.test import Client


class CarListTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get("/fleet/vehicule")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)


class CarDetailTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get("/fleet/vehicule/1")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)


class DriverListTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get("/fleet/chauffeur")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)


class ContractListTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get("/fleet/contrat")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)
