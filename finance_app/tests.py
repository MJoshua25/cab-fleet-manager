import unittest
from django.test import Client


class OutageListTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get("/finance/panne")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)


class InsuranceListTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get("/finance/assurance")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)


class InsurancePaymentListTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get("/finance/paiement_assurance")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)


class OilChangeListTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get("/finance/vidange")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)