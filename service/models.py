"""
Models for YourResourceModel

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """


class Customer(db.Model):
    """
    Class that represents a customers
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(63), nullable=False)
    lastname = db.Column(db.String(63), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    street_line1 = db.Column(db.String(256), nullable=False)
    street_line2 = db.Column(db.String(256), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(46), nullable=False)
    country = db.Column(db.String(93), nullable=False)
    zipcode = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
        server_onupdate=db.func.now()
        )
    acc_active = db.Column(db.Boolean, server_default=db.true(), nullable=False)

    def __repr__(self):
        cust = "<Customer %r id=[%s] acc_active=[%s]>" % (self.firstname, self.id, self.acc_active)
        return cust

    def create(self):
        """
        Creates a Customer to the database
        """
        logger.info("Creating %s", self.firstname)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Customer to the database
        """
        logger.info("Saving %s", self.firstname)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ Removes a Customer from the data store """
        logger.info("Deleting %s", self.firstname)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "phone": self.phone,
            "street_line1": self.street_line1,
            "street_line2": self.street_line2,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "zipcode": self.zipcode,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "acc_active": self.acc_active
        }

    def deserialize(self, data):
        """
        Deserializes a Customer from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.firstname = data["firstname"]
            self.lastname = data["lastname"]
            self.email = data["email"]
            self.phone = data["phone"]
            self.street_line1 = data["street_line1"]
            self.street_line2 = data["street_line2"]
            self.city = data["city"]
            self.state = data["state"]
            self.country = data["country"]
            self.zipcode = data["zipcode"]
            self.created_at = data.get("created_at")
            self.updated_at = data.get("updated_at")
            self.acc_active = data.get("acc_active")
        except KeyError as error:
            raise DataValidationError(
                "Invalid Customer: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Customer: body of request contained bad or no data - "
                "Error message: " + error.args[0]
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Customers in the database """
        logger.info("Processing all YourResourceModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Customer by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, firstname):
        """Returns all Customers with the given firstname

        Args:
            firstname (string): the firstname of the Customers you want to match
        """
        logger.info("Processing firstname query for %s ...", firstname)
        return cls.query.filter(cls.firstname == firstname)

    @classmethod
    def find_by_email(cls, email):
        """Returns the first Customer with the given email

        Args:
            email (string): the email of the Customers you want to match
        """
        logger.info("Processing email query for %s ...", email)
        return cls.query.filter(cls.email == email).first()
