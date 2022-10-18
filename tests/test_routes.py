"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
from email.mime import application
import json
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import app
from service.models import Customer, db
from service.common import status
from tests.factories import CustomerFactory  # HTTP Status Codes

BASE_URL = "/customers"

######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        pass

    ######################################################################
    #  C U S T O M E R S   T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_customer(self):
        """ It should create a customer"""
        customer = CustomerFactory()
        logging.debug(customer)
        resp = self.app.post(
            BASE_URL, json=customer.serialize(), content_type="application/json"
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, "Account not created")
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_customer = resp.get_json()
        self.assertEqual(
            new_customer["firstname"], customer.firstname, "First names does not match"
        )
        self.assertEqual(new_customer["lastname"], customer.lastname, "Last names does not match")
        self.assertEqual(new_customer["email"], customer.email, "Email does not match")
        self.assertEqual(new_customer["phone"], customer.phone, "Phone number does not match")
        self.assertEqual(
            new_customer["street_line1"], customer.street_line1, "Street line 1 does not match"
        )
        self.assertEqual(
            new_customer["street_line2"], customer.street_line2, "Street line 2 does not match"
        )
        self.assertEqual(new_customer["city"], customer.city, "City does not match")
        self.assertEqual(new_customer["state"], customer.state, "State does not match")
        self.assertEqual(new_customer["country"], customer.country, "Country does not match")
        self.assertEqual(new_customer["zipcode"], customer.zipcode, "Zipcode does not match")

        self.assertEqual(
            new_customer["created_at"],
            customer.created_at.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            "Date created at does not match",
        )

        self.assertEqual(
            new_customer["updated_at"],
            customer.updated_at.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            "Date updated at does not match",
        )

        # Check that the location header was correct by getting it
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK, "Header account not created")
        new_customer = resp.get_json()
        self.assertEqual(
            new_customer["firstname"], customer.firstname, "First names does not match"
        )
        self.assertEqual(new_customer["lastname"], customer.lastname, "Last names does not match")
        self.assertEqual(new_customer["email"], customer.email, "Email does not match")
        self.assertEqual(new_customer["phone"], customer.phone, "Phone number does not match")
        self.assertEqual(
            new_customer["street_line1"], customer.street_line1, "Street line 1 does not match"
        )
        self.assertEqual(
            new_customer["street_line2"], customer.street_line2, "Street line 2 does not match"
        )
        self.assertEqual(new_customer["city"], customer.city, "City does not match")
        self.assertEqual(new_customer["state"], customer.state, "State does not match")
        self.assertEqual(new_customer["country"], customer.country, "Country does not match")
        self.assertEqual(new_customer["zipcode"], customer.zipcode, "Zipcode does not match")

        self.assertEqual(
            new_customer["created_at"],
            customer.created_at.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            "Date created at does not match",
        )

        self.assertEqual(
            new_customer["updated_at"],
            customer.updated_at.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            "Date updated at does not match",
        )

    def test_bad_request(self):
        """It should not Create when sending the wrong data"""
        resp = self.app.post(BASE_URL, json={"name": "not enough data"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsupported_media_type(self):
        """It should not Create when sending wrong media type"""
        customer = CustomerFactory()
        resp = self.app.post(
            BASE_URL, json=customer.serialize(), content_type="test/html"
        )
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
