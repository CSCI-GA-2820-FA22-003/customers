"""
My Service

Describe what your service does here
"""

# from tkinter import E
from flask import jsonify, request, make_response
from flask_restx import fields, reqparse, inputs, Resource
from service.models import Customer
from .common import status  # HTTP Status Codes

# Import Flask application
from . import app, api

######################################################################
# GET INDEX
######################################################################


@app.route("/")
def index():
    """Base URL for our service"""
    app.logger.info("Base URL")
    return app.send_static_file("index.html")

######################################################################
# Configure the Root route before OpenAPI
######################################################################


# Define the model so that the docs reflect what can be sent
create_model = api.model('Customer', {
    'firstname': fields.String(required=True, description='The first name of the Customer'),
    'lastname': fields.String(required=True, description='The last name of the Customer'),
    'email': fields.String(required=True, description='The email of the Customer'),
    'phone': fields.String(required=True, description='The phone of the Customer'),
    'street_line1': fields.String(required=True, description='The street_line1 of the Customer'),
    'street_line2': fields.String(required=True, description='The street_line2 of the Customer'),
    'city': fields.String(required=True, description='The city of the Customer'),
    'state': fields.String(required=True, description='The state of the Customer'),
    'country': fields.String(required=True, description='The country of the Customer'),
    'zipcode': fields.String(required=True, description='The zipcode of the Customer'),
    'created_at': fields.Date(required=True, description='The time when Customer was created'),
    'updated_at': fields.Date(required=True, description='The time when Customer was deleted'),
    'acc_active': fields.Boolean(required=True, description='Is the Customer account active'),
})

customer_model = api.inherit(
    'CustomerModel',
    create_model,
    {
        'id': fields.String(readOnly=True, description='The unique id assigned internally by service'),
    }
)

# query string arguments
customer_args = reqparse.RequestParser()
customer_args.add_argument('name', type=str, location='args', required=False, help='List Customers by name')
customer_args.add_argument('acc_active', type=inputs.boolean, location='args',
                           required=False, help='List Customers by their active status')

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


def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)


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
#  PATH: /customers/{id}
######################################################################


@api.route('/customers/<customer_id>')
@api.param('customer_id', 'The Customer identifier')
class CustomerResource(Resource):
    """
    CustomerResource class
    Allows the manipulation of a single Customer
    GET /customer{id} - Returns a Customer with the id
    PUT /customer{id} - Update a Customer with the id
    DELETE /customer{id} -  Deletes a Customer with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A CUSTOMER
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING CUSTOMER
    # ------------------------------------------------------------------

    # @app.route("/api/customers/<int:customer_id>", methods=["PUT"])
    @api.doc('update_customer')
    @api.response(404, 'Customer not found')
    @api.expect(customer_model)
    @api.marshal_with(customer_model)
    def put(self, customer_id):
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
        customer_account.lastname = customer_account.lastname.title()
        customer_account.email = customer_account.email.lower()
        customer_account.city = customer_account.city.title()
        customer_account.update()
        return customer_account.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A CUSTOMER
    # ------------------------------------------------------------------


######################################################################
#  PATH: /customers
######################################################################
@api.route('/customers', strict_slashes=False)
class CustomerCollection(Resource):
    """ Handles all interactions with collections of Customers """

    # ------------------------------------------------------------------
    # LIST ALL CUSTOMERS
    # ------------------------------------------------------------------

    @api.doc('list_customers')
    @api.expect(customer_args, validate=True)
    @api.marshal_list_with(customer_model)
    def get(self):
        """Returns all of the Customers"""
        app.logger.info("Request for all Customers")
        customers = []
        lastname = request.args.get("lastname")
        city = request.args.get("city")
        email = request.args.get("email")
        firstname = request.args.get("firstname")
        if lastname:
            customers = Customer.find_by_lastname(lastname)
        elif firstname:
            customers = Customer.find_by_firstname(firstname)
        elif city:
            customers = Customer.find_by_city(city)
        elif email:
            customers = Customer.find_by_email(email)
        else:
            customers = Customer.all()

        results = [customer.serialize() for customer in customers]
        app.logger.info("Returning %d customers", len(results))
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # CREATE A NEW CUSTOMER
    # ------------------------------------------------------------------
    @api.doc('create_customers')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(customer_model, code=201)
    def post(self):
        """
        Creates a Customer
        This endpoint will create a Customer based on the data
        in the body that is posted
        """
        app.logger.info("Request to create a Customer")
        check_content_type("application/json")
        customer = Customer()
        app.logger.debug('Payload = %s', api.payload)
        customer.deserialize(api.payload)

        # Setting to lower case for optimal possible case insensitive email queries later on
        customer.email = customer.email.lower()
        # Setting to title case for optimal possible case insensitive
        # lastname and city queries later on
        customer.lastname = customer.lastname.title()
        customer.city = customer.city.title()

        if check_for_dupe_emails(customer.email):
            abort(
                status.HTTP_409_CONFLICT,
                f"Another Customer with email '{customer.email}' found.",
            )

        customer.create()
        # Create a message to return
        # message = customer.serialize()
        location_url = api.url_for(CustomerResource, customer_id=customer.id, _external=True)

        app.logger.info('Customer with new id [%s] created!', customer.id)
        return customer.serialize(), status.HTTP_201_CREATED, {'Location': location_url}


######################################################################
#  PATH: /customers/{id}/activate
######################################################################
@api.route('/customers/<customer_id>/active')
@api.param('customer_id', 'The Customer identifier')
class ActivateResource(Resource):
    """ Activate actions on Customers """

    # ------------------------------------------------------------------
    # ACTIVATE A CUSTOMER
    # ------------------------------------------------------------------

    @api.doc('activate_customer')
    @api.response(404, 'Customer not found')
    def put(self, customer_id):
        """
        Activates a Customer
        This endpoint will Activate a Customer based on the id specified in the path
        """
        app.logger.info("Request to Activate a customer with id: %s", customer_id)
        check_content_type("application/json")
        customer = Customer.find(customer_id)
        if not customer:
            abort(status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' was not found.")

        customer.acc_active = True
        customer.update()
        app.logger.info("Customer with ID [%s] activation complete.", customer_id)
        return customer.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DEACTIVATE A CUSTOMER
    # ------------------------------------------------------------------


######################################################################
# READ A CUSTOMER
######################################################################


@app.route("/api/customers/<int:customer_id>", methods=["GET"])
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
# DELETE A CUSTOMER
######################################################################


@app.route("/api/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """ Delete a Customer """
    app.logger.info("Request to delete customer with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if customer:
        customer.delete()
        app.logger.info("Customer with ID [%s] delete complete.", customer_id)
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# DEACTIVATE A CUSTOMER'S ACCOUNT
######################################################################


@app.route("/api/customers/<int:customer_id>/active", methods=["DELETE"])
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
