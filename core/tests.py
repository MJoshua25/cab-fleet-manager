import unittest
from django.test import Client


class RegistrationTest(unittest.TestCase):
	def setUp(self):
		# Every test needs a client.
		self.client = Client()

	def test_details(self):
		# Issue a GET request.
		response = self.client.get("/inscription")

		# Check that the response is 200 OK.
		self.assertEqual(response.status_code, 200)


class LoginTest(unittest.TestCase):
	def setUp(self):
		# Every test needs a client.
		self.client = Client()

	def test_details(self):
		# Issue a GET request.
		response = self.client.get("/connexion")

		# Check that the response is 200 OK.
		self.assertEqual(response.status_code, 200)
