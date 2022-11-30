"""
My Service

Describe what your service does here
"""

# from tkinter import E
from flask import jsonify, request, url_for, make_response, abort
from service.models import Customer
from .common import status  # HTTP Status Codes

# Import Flask application
from . import app

############################################################
# H E A L T H   E N D P O I N TS
############################################################


@app.route("/health")
def health():
    """Health Status"""
    app.logger.info("Service active, health endpoint successfully called")
    return jsonify(dict(status="OK")), status.HTTP_200_OK

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_for_dupe_emails(customer_email):
    """
    Retrieve a single Customer by email address
    This endpoint will return a Customer based on it's email
    """
    app.logger.info("Request for Customer with email: %s", customer_email)
    # See if the Customer exists
    customer = Customer.find_by_email(customer_email).first()
    if customer:
        return True
    return False


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Customer.init_db(app)

######################################################################
# GET INDEX
######################################################################


@app.route("/")
def index():
    """Base URL for our service"""
    app.logger.info("Base URL")
    return app.send_static_file("index.html")

######################################################################
# CREATE A NEW CUSTOMER
######################################################################


@app.route("/customers", methods=["POST"])
def create_customers():
    """
    Creates a Customer
    This endpoint will create a Customer based on the data in the body that is posted
    """
    app.logger.info("Request to create an Customer")
    check_content_type("application/json")

    # Create the account
    customer = Customer()
    customer.deserialize(request.get_json())

    # Setting to lower case for optimal possible case insensitive email queries later on
    customer.email = customer.email.lower()

    if check_for_dupe_emails(customer.email):
        abort(
            status.HTTP_409_CONFLICT,
            f"Another Customer with email '{customer.email}' found.",
        )

    customer.create()

    # Create a message to return
    message = customer.serialize()
    # Change to "get customer" when it is made
    location_url = url_for("get_customer", customer_id=customer.id, _external=True)

    app.logger.info("Customer with ID [%s] created.", customer.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# READ A CUSTOMER
######################################################################


@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    """
    Retrieve a single Customer
    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request for Customer with id: %s", customer_id)

    # See if the Customer exists and abort if it doesn't
    customer = Customer.find(customer_id)
    if not customer:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Customer with id '{customer_id}' could not be found.",
        )

    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)

######################################################################
# LIST ALL CUSTOMERS
######################################################################


@app.route("/customers", methods=["GET"])
def list_customers():
    """Returns all of the Customers"""
    app.logger.info("Request for all Customers")
    customers = []
    lastname = request.args.get("lastname")
    city = request.args.get("city")
    email = request.args.get("email")
    if lastname:
        customers = Customer.find_by_lastname(lastname)
    elif city:
        customers = Customer.find_by_city(city)
    elif email:
        customers = Customer.find_by_email(email)
    else:
        customers = Customer.all()

    results = [customer.serialize() for customer in customers]
    app.logger.info("Returning %d customers", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# DELETE A CUSTOMER
######################################################################


@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """ Delete a Customer """
    app.logger.info("Request to delete customer with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if customer:
        customer.delete()
        app.logger.info("Customer with ID [%s] delete complete.", customer_id)
    return "", status.HTTP_204_NO_CONTENT

######################################################################
# REST API TO UPDATE CUSTOMER'S PERSONAL DATA
######################################################################


@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    """
    Update a customer's personal data.
    This endpoint will update a customer's data based on the body that is posted
    """
    app.logger.info("Request to update the customer with id: %s", customer_id)
    check_content_type("application/json")

    # See if the account exists and abort if it doesn't
    customer_account = Customer.find(customer_id)
    if not customer_account:
        abort(
            status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' was not found."
        )

    # Update from the json in the body of the request
    customer_account.deserialize(request.get_json())
    customer_account.id = customer_id
    customer_account.email = customer_account.email.lower()
    customer_account.update()

    return make_response(jsonify(customer_account.serialize()), status.HTTP_200_OK)

######################################################################
# ACTIVATE A CUSTOMER'S ACCOUNT
######################################################################


@app.route("/customers/<int:customer_id>/active", methods=["PUT"])
def activate_customer_account(customer_id):
    """
    Activate a customer's account
    """
    app.logger.info("Request to activate the customer with id: %s", customer_id)
    check_content_type("application/json")

    # See if the account exists and abort if it doesn't
    customer_account = Customer.find(customer_id)
    if not customer_account:
        abort(
            status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' was not found."
        )

    customer_account.acc_active = True
    customer_account.update()

    return make_response(jsonify(customer_account.serialize()), status.HTTP_200_OK)

######################################################################
# DEACTIVATE A CUSTOMER'S ACCOUNT
######################################################################


@app.route("/customers/<int:customer_id>/active", methods=["DELETE"])
def deactivate_customer_account(customer_id):
    """
    Deactivate a customer's account
    """
    app.logger.info("Request to deactivate the customer with id: %s", customer_id)
    check_content_type("application/json")

    # See if the account exists and abort if it doesn't
    customer_account = Customer.find(customer_id)
    if not customer_account:
        abort(
            status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' was not found."
        )

    customer_account.acc_active = False
    customer_account.update()

    return make_response(jsonify(customer_account.serialize()), status.HTTP_200_OK)
