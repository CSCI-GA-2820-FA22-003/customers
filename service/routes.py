"""
My Service

Describe what your service does here
"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from .common import status  # HTTP Status Codes
from service.models import Customer

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


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
    customer_account.update()

    return make_response(jsonify(customer_account.serialize()), status.HTTP_200_OK)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


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
