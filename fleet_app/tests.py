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
        self.assertEqual(response.status_code, 200)


class CarModifTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get("/fleet/vehicule/modif_vehicule")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


