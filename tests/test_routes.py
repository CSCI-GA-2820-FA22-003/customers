"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
# from email.mime import application
# import json
# import os
import logging
from unittest import TestCase
# from unittest.mock import MagicMock, patch
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
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.commit()
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  H E L P E R   M E T H O D S
    ######################################################################

    def _create_customers(self, count):
        """Factory method to create customers in bulk"""
        customers = []
        for _ in range(count):
            test_customer = CustomerFactory()
            response = self.app.post(BASE_URL, json=test_customer.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test customer"
            )
            new_customer = response.get_json()
            test_customer.id = new_customer["id"]
            customers.append(test_customer)
        return customers

    ######################################################################
    #  C U S T O M E R S   T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_customer_list(self):
        """It should Get a list of Customers"""
        self._create_customers(5)
        resp = self.app.get(BASE_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

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

    def test_get_customer(self):
        """It should Read a single customer"""
        # get the id of an account

        customer = self._create_customers(1)[0]
        resp = self.app.get(
            f"{BASE_URL}/{customer.id}", content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()

        self.assertEqual(data["firstname"], customer.firstname)

    def test_get_customer_not_found(self):
        """It should not Read a Customer that is not found"""
        resp = self.app.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_not_supported(self):
        """It should not allow an illegal method call"""
        resp = self.app.put(BASE_URL, json={"not": "today"})
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
