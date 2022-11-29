Feature: The customers service back-end
    As a Customer Website
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
        | ID   | Firstname   | Lastname   | Email            | Phone       | Street_Line1   | Street_Line2        | City            | State     | Country   | Zipcode   |
        | 1    | Temp        | Rary       | tr99@gmail.com   | 123456789   | 221B           | Baker St            | London          | England   | UK        | NW1       |
        | 2    | Psudo       | Nim        | pn25@gmail.com   | 999999999   | 350            | Fifth Avenue        | New York City   | New York  | USA       | 10118     |
        | 3    | Adi         | Rang       | ar01@gmail.com   | 333555888   | 742            | Evergreen Terrace   | Springfield     | Oregon    | USA       | 42659     |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customers RESTful Service" in the title
    And I should not see "404 Not Found"

# I need create to work for this.
Scenario: Retrieve a Customer
    When I visit the "Home Page"
    # Create the customer here and get its ID copy/paste 
    # to ID test retrieve...
    And I set the "ID" to "1"
    And I press the "Retrieve" button
    Then I should see the message "Success"
    # And I should see "Temp" in the "Firstname" field
    # And I should see "Rary" in the "Lastname" field
    # And I should see "tr99@gmail.com" in the "Email" field
    # And I should see "123456789" in the "Phone" field
    # And I should see "221B" in the "Street_Line1" field
    # And I should see "Baker St" in the "Street_Line2" field
    # And I should see "London" in the "City" field
    # And I should see "England" in the "State" field
    # And I should see "UK" in the "Country" field
    # And I should see "NW1" in the "Zipcode" field
    