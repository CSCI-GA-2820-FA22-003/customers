import factory
from service.models import Customer

class CustomerFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Customer

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")
    lastname = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    address = factory.Faker("street_address")
    city = factory.Faker("city")
    state = factory.Faker("state_abbr")
    country = factory.Faker("country")
    zipcode = factory.Faker("postalcode")