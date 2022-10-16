"""
Test cases for Customer Model

"""
import os
import logging
import unittest
from service import app
from service.models import Customer, DataValidationError, db
from tests.factories import CustomerFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  C U S T O M E R   M O D E L   T E S T   C A S E S
######################################################################
class TestCustomer(unittest.TestCase):
    """ Test Cases for Customer Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Customer.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_customer(self):
        """ It should Create an Customer and assert that it exists """
        customer = Customer(name="Katerine",lastname="Perdomo",email="kate@email.com",phone="XXXXXX",address1="casa",address2="casa",city="Bogota",state='CU',country="Colombia",zipcode="11023")
        self.assertTrue(customer is not None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.name, "Katerine")
        self.assertEqual(customer.lastname, "Perdomo")
        self.assertEqual(customer.email, "kate@email.com")
        self.assertEqual(customer.phone, "XXXXXX")
        self.assertEqual(customer.address1, "casa")
        self.assertEqual(customer.address2, "casa")
        self.assertEqual(customer.state, "CU")
        self.assertEqual(customer.country, "Colombia")
        self.assertEqual(customer.zipcode, "11023")

    def test_add_a_customer(self):
        """It should Create a customer and add it to the database"""
        customers = Customer.all()
        self.assertEqual(customers, [])
        customer = Customer(name="Katerine",lastname="Perdomo",email="kate@email.com",phone="XXXXXX",address1="casa",address2="casa",city="Bogota",state='CU',country="Colombia",zipcode="11023")
        self.assertTrue(customer is not None)
        self.assertEqual(customer.id, None)
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(customer.id)
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
    
    def test_read_a_customer(self):
        """It should Read a Customer"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        customer.create()
        self.assertIsNotNone(customer.id)
        # Fetch it back
        found_customer = Customer.find(customer.id)
        self.assertEqual(found_customer.id, found_customer.id)
        self.assertEqual(found_customer.name, found_customer.name)
        self.assertEqual(found_customer.lastname, customer.lastname)
        self.assertEqual(found_customer.address1, customer.address1)

    def test_update_a_customer(self):
        """It should Update a Customer"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        customer.create()
        logging.debug(customer)
        self.assertIsNotNone(customer.id)
        # Change it and save it
        customer.lastname = "Moreno"
        original_id = customer.id
        customer.update()
        self.assertEqual(customer.id, original_id)
        self.assertEqual(customer.lastname, "Moreno")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].id, original_id)
        self.assertEqual(customers[0].lastname, "Moreno")

    def test_update_no_id(self):
        """It should not Update a Customer with no id"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        self.assertRaises(DataValidationError, customer.update)
    
    def test_delete_a_customer(self):
        """It should Delete a Customer"""
        customer = CustomerFactory()
        customer.create()
        self.assertEqual(len(Customer.all()), 1)
        # delete the customer and make sure it isn't in the database
        customer.delete()
        self.assertEqual(len(Customer.all()), 0)
    
    def test_list_all_customers(self):
        """It should List all Customers in the database"""
        customers = Customer.all()
        self.assertEqual(customers, [])
        num_new_customers = 5
        # Create 5 Customers
        for _ in range(num_new_customers):
            customer = CustomerFactory()
            customer.create()
        # See if we get back 5 customers
        customers = Customer.all()
        self.assertEqual(len(customers), num_new_customers)

    def test_serialize_a_customer(self):
        """It should serialize a Customer"""
        customer = CustomerFactory()
        data = customer.serialize()
        self.assertEqual(data["id"], customer.id)
        self.assertEqual(data["name"], customer.name)
        self.assertEqual(data["lastname"], customer.lastname)
        self.assertEqual(data["email"], customer.email)
        self.assertEqual(data["phone"], customer.phone)
        self.assertEqual(data["address1"], customer.address1)
        self.assertEqual(data["address2"], customer.address2)
        self.assertEqual(data["city"], customer.city)
        self.assertEqual(data["state"], customer.state)
        self.assertEqual(data["country"], customer.country) 
        self.assertEqual(data["zipcode"], customer.zipcode) 
        self.assertEqual(data["created_at"], customer.created_at)  
        self.assertEqual(data["updated_at"], customer.updated_at)  
    
    def test_deserialize_a_customer(self):
        """It should de-serialize a Customer"""
        data = CustomerFactory().serialize()
        customer = Customer()
        customer.deserialize(data)
        self.assertNotEquals(customer, None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.name, data["name"])
