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

# Add UI Scenarios here
