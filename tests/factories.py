
import factory
from service.models import Customer
from factory.fuzzy import FuzzyDate
from datetime import date

class CustomerFactory(factory.Factory):
    """Creates fake customer that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Customer

    id = factory.Sequence(lambda n: n)
    firstname = factory.Faker("first_name")
    lastname = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    street_line1 = factory.Faker("street_address")
    street_line2 = factory.Faker("street_address")
    city = factory.Faker("city")
    state = factory.Faker("state_abbr")
    country = factory.Faker("country")
    zipcode = factory.Faker("postalcode")
    created_at = FuzzyDate(date(2022, 1, 1))
    updated_at = FuzzyDate(date(2022, 1, 1))