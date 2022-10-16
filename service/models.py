"""
Models for YourResourceModel

All of the models are stored in this module
"""
from email.policy import default
import logging
from time import timezone
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import func

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
    name = db.Column(db.String(63),nullable=False)
    lastname = db.Column(db.String(63),nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(60))
    address1 = db.Column(db.String(256))
    address2 = db.Column(db.String(256))
    city = db.Column(db.String(64))
    state = db.Column(db.String(16))
    country = db.Column(db.String(63))
    zipcode = db.Column(db.String(60))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now) 


    def __repr__(self):
        return "<Customer %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a Customer to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Customer to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ Removes a Customer from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        return {"id": self.id, 
                "name": self.name,
                "lastname": self.lastname,
                "email": self.email,
                "phone": self.phone,
                "address1": self.address1,
                "address2": self.address2,
                "city": self.city,
                "state": self.state,
                "country": self.country,
                "zipcode": self.zipcode,
                "created_at":self.created_at,
                "updated_at":self.updated_at
                }

    def deserialize(self, data):
        """
        Deserializes a Customer from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.lastname = data["lastname"]
            self.email = data["email"]
            self.phone = data["phone"]
            self.address1 = data["address1"]
            self.address2 = data["address2"]
            self.city = data["city"]
            self.state = data["state"]
            self.country = data["country"]
            self.zipcode = data["zipcode"]
            self.created_at = data["created_at"]
            self.updated_at =data["updated_at"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Customer: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Customer: body of request contained bad or no data - "
                "Error message: " + error
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
    def find_by_name(cls, name):
        """Returns all Customers with the given name

        Args:
            name (string): the name of the Customers you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
