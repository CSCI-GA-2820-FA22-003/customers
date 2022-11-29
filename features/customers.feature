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
    And I set the "Firstname" to "Burt"
    And I set the "Lastname" to "Smith"
    And I set the "Email" to "burt@smith.com"
    And I set the "Phone" to "0987654321"
    And I set the "Street Line1" to "25 Long Drive"
    And I set the "Street Line2" to "2nd Street"
    And I set the "City" to "London"
    And I set the "State" to "London"
    And I set the "Country" to "UK"
    And I set the "Zipcode" to "098765"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Firstname" field should be empty
    And the "Lastname" field should be empty
    And the "Email" field should be empty
    And the "Phone" field should be empty
    And the "Street Line1" field should be empty
    And the "Street Line2" field should be empty
    And the "City" field should be empty
    And the "State" field should be empty
    And the "Country" field should be empty
    And the "Zipcode" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Burt" in the "Firstname" field
    And I should see "Smith" in the "Lastname" field
    And I should see "burt@smith.com" in the "Email" field
    And I should see "0987654321" in the "Phone" field
    And I should see "25 Long Drive" in the "Street Line1" field
    And I should see "2nd Street" in the "Street Line2" field
    And I should see "London" in the "City" field
    And I should see "London" in the "State" field
    And I should see "UK" in the "Country" field
    And I should see "098765" in the "Zipcode" field

    
Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "Firstname" to "Burt"
    And I set the "Lastname" to "Smith"
    And I set the "Email" to "burt@smith.com"
    And I set the "Phone" to "0987654321"
    And I set the "Street Line1" to "25 Long Drive"
    And I set the "Street Line2" to "2nd Street"
    And I set the "City" to "London"
    And I set the "State" to "London"
    And I set the "Country" to "UK"
    And I set the "Zipcode" to "098765"
    And I press the "Create" button
    Then I should see the message "Success"

Scenario: Create a Customer with a bad email
    When I visit the "Home Page"
    And I set the "Firstname" to "Burt"
    And I set the "Lastname" to "Smith"
    And I set the "Email" to "BAD_EMAIL_FORMAT"
    And I set the "Phone" to "0987654321"
    And I set the "Street Line1" to "25 Long Drive"
    And I set the "Street Line2" to "2nd Street"
    And I set the "City" to "London"
    And I set the "State" to "London"
    And I set the "Country" to "UK"
    And I set the "Zipcode" to "098765"
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "This doesn't appear to be a valid email address" in the "Email" error string

Scenario: Attempt to create a Customer with missing Firstname data
    When I visit the "Home Page"
    And I set the "Lastname" to "Smith"
    And I set the "Email" to "burt@smith.com"
    And I set the "Phone" to "0987654321"
    And I set the "Street Line1" to "25 Long Drive"
    And I set the "Street Line2" to "2nd Street"
    And I set the "City" to "London"
    And I set the "State" to "London"
    And I set the "Country" to "UK"
    And I set the "Zipcode" to "098765"
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "Firstname" error string
    When I set the "Firstname" to "Burt"
    And I press the "Create" button
    Then The "Firstname" error string should be gone

Scenario: Attempt to create a Customer with missing Lastname data
    When I visit the "Home Page"
    And I set the "Firstname" to "Burt"
    And I set the "Email" to "burt@smith.com"
    And I set the "Phone" to "0987654321"
    And I set the "Street Line1" to "25 Long Drive"    
    And I set the "Street Line2" to "2nd Street"
    And I set the "City" to "London"
    And I set the "State" to "London"
    And I set the "Country" to "UK"
    And I set the "Zipcode" to "098765"
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "Lastname" error string
    When I set the "Lastname" to "Smith"
    And I press the "Create" button
    Then The "Lastname" error string should be gone

Scenario: Attempt to create a Customer with missing Email data
    When I visit the "Home Page"
    And I set the "Firstname" to "Burt"
    And I set the "Lastname" to "Smith"
    And I set the "Phone" to "0987654321"    
    And I set the "Street Line1" to "25 Long Drive"    
    And I set the "Street Line2" to "2nd Street"
    And I set the "City" to "London"
    And I set the "State" to "London"
    And I set the "Country" to "UK"
    And I set the "Zipcode" to "098765"
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "Email" error string
    When I set the "Email" to "burt@smith.com"
    And I press the "Create" button
    Then The "Email" error string should be gone

Scenario: Attempt to create a Customer with missing Phone data
    When I visit the "Home Page"
    And I set the "Firstname" to "Burt"
    And I set the "Lastname" to "Smith"
    And I set the "Email" to "burt@smith.com"    
    And I set the "Street Line1" to "25 Long Drive"    
    And I set the "Street Line2" to "2nd Street"
    And I set the "City" to "London"
    And I set the "State" to "London"
    And I set the "Country" to "UK"
    And I set the "Zipcode" to "098765"
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "Phone" error string
    When I set the "Phone" to "098765432"
    And I press the "Create" button
    Then The "Phone" error string should be gone

Scenario: Attempt to create a Customer with missing Street Line1 data
    When I visit the "Home Page"
    And I set the "Firstname" to "Burt"
    And I set the "Lastname" to "Smith"
    And I set the "Email" to "burt@smith.com"   
    And I set the "Phone" to "0987654321"        
    And I set the "Street Line2" to "2nd Street"
    And I set the "City" to "London"
    And I set the "State" to "London"
    And I set the "Country" to "UK"
    And I set the "Zipcode" to "098765"
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "Street Line1" error string
    When I set the "Street Line1" to "25 Long Drive"
    And I press the "Create" button
    Then The "Street Line1" error string should be gone    

Scenario: Attempt to create a Customer with missing Street Line2 data
    When I visit the "Home Page"
    And I set the "Firstname" to "Burt"
    And I set the "Lastname" to "Smith"
    And I set the "Email" to "burt@smith.com"   
    And I set the "Phone" to "0987654321"
    And I set the "Street Line1" to "25 Long Drive"
    And I set the "City" to "London"
    And I set the "State" to "London"
    And I set the "Country" to "UK"
    And I set the "Zipcode" to "098765"
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "Street Line2" error string
    When I set the "Street Line2" to "2nd Street"
    And I press the "Create" button
    Then The "Street Line2" error string should be gone

Scenario: Attempt to create a Customer with missing City data
    When I visit the "Home Page"
    And I set the "Firstname" to "Burt"
    And I set the "Lastname" to "Smith"
    And I set the "Email" to "burt@smith.com"   
    And I set the "Phone" to "0987654321"
    And I set the "Street Line1" to "25 Long Drive"
    And I set the "Street Line2" to "2nd Street"    
    And I set the "State" to "London"
    And I set the "Country" to "UK"
    And I set the "Zipcode" to "098765"
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "City" error string
    When I set the "City" to "London"
    And I press the "Create" button
    Then The "City" error string should be gone   

Scenario: Attempt to create a Customer with missing State data
    When I visit the "Home Page"
    And I set the "Firstname" to "Burt"
    And I set the "Lastname" to "Smith"
    And I set the "Email" to "burt@smith.com"   
    And I set the "Phone" to "0987654321"
    And I set the "Street Line1" to "25 Long Drive"
    And I set the "Street Line2" to "2nd Street"   
    And I set the "City" to "London"    
    And I set the "Country" to "UK"
    And I set the "Zipcode" to "098765"
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "State" error string
    When I set the "State" to "London"
    And I press the "Create" button
    Then The "State" error string should be gone    

Scenario: Attempt to create a Customer with missing Country data
    When I visit the "Home Page"
    And I set the "Firstname" to "Burt"
    And I set the "Lastname" to "Smith"
    And I set the "Email" to "burt@smith.com"   
    And I set the "Phone" to "0987654321"
    And I set the "Street Line1" to "25 Long Drive"
    And I set the "Street Line2" to "2nd Street"   
    And I set the "City" to "London"    
    And I set the "State" to "London"    
    And I set the "Zipcode" to "098765"
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "Country" error string
    When I set the "Country" to "UK"
    And I press the "Create" button
    Then The "Country" error string should be gone    

Scenario: Attempt to create a Customer with missing Zipcode data
    When I visit the "Home Page"
    And I set the "Firstname" to "Burt"
    And I set the "Lastname" to "Smith"
    And I set the "Email" to "burt@smith.com"   
    And I set the "Phone" to "0987654321"
    And I set the "Street Line1" to "25 Long Drive"
    And I set the "Street Line2" to "2nd Street"   
    And I set the "City" to "London"    
    And I set the "State" to "London"  
    And I set the "Country" to "UK"
    And I press the "Create" button
    Then I should see the message "Form Error(s)"
    And I should see "Required field" in the "Zipcode" error string
    When I set the "Zipcode" to "098765"
    And I press the "Create" button
    Then The "Zipcode" error string should be gone

Scenario: Search Customers by City
    When I visit the "Home Page"
    And I set the "City" to "London"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Rary" in the results
    And I should not see "Nim" in the results
    And I should not see "Rang" in the results