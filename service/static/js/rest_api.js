$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_id").val(res.id);
        $("#customer_firstname").val(res.firstname);
        $("#customer_lastname").val(res.lastname);
        $("#customer_email").val(res.email);
        $("#customer_phone").val(res.phone);
        $("#customer_street_line1").val(res.street_line1);
        $("#customer_street_line2").val(res.street_line2);
        $("#customer_city").val(res.city);
        $("#customer_state").val(res.state);
        $("#customer_country").val(res.country);
        $("#customer_zipcode").val(res.zipcode);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#customer_id").val("");
        $("#customer_firstname").val("");
        $("#customer_lastname").val("");
        $("#customer_email").val("");
        $("#customer_phone").val("");
        $("#customer_street_line1").val("");
        $("#customer_street_line2").val("");
        $("#customer_city").val("");
        $("#customer_state").val("");
        $("#customer_country").val("");
        $("#customer_zipcode").val("");        
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // Function to regex check the format of the email
    function validateEmail($email) {
        let emailReg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return emailReg.test($email);
    }

    // ****************************************
    // Create a Customer
    // ****************************************

    $("#create-btn").click(function () {

        let firstname = $("#customer_firstname").val().trim();
        let lastname = $("#customer_lastname").val().trim();
        let email = $("#customer_email").val().trim();
        let phone = $("#customer_phone").val().trim();
        let street_line1 = $("#customer_street_line1").val().trim();
        let street_line2 = $("#customer_street_line2").val().trim();
        let city = $("#customer_city").val().trim();
        let state = $("#customer_state").val().trim();
        let country = $("#customer_country").val().trim();
        let zipcode = $("#customer_zipcode").val().trim();
      
        let data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "phone": phone,
            "street_line1": street_line1,
            "street_line2": street_line2,
            "city": city,
            "state": state,
            "country": country,
            "zipcode": zipcode,  
        };

        // Check for missing required data in form
        dataError = 0
        for (let i in data) {
            input = "#customer_"+i
            if (!data[i]) {
                $(input).closest(".form-group").addClass("has-error");
                $(input+"_err p").html("");
                $(input+"_err p").text("Required field").show();
                dataError++
            } else {
                $(input).closest(".form-group").removeClass("has-error");
                $(input+"_err p").html("");
                $(input+"_err p").hide();
            }
        }

        // Validate the email address
        if (email) {
            if (!validateEmail(email)) {
                input = "#customer_email"
                $(input).closest(".form-group").addClass("has-error");
                $(input+"_err p").html("");
                $(input+"_err p").append("This doesn't appear to be a valid email address").show();        
                dataError++
            }
        }

        // Stop the execution of the script if there are data errors
        if (dataError > 0) {
            $("#flash_message").html("Form Error(s)")
            return false
        }
        
        $("#flash_message").empty();
        
        // Send the form data to the API
        let ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Customer
    // ****************************************

    // ****************************************
    // Retrieve a Customer
    // ****************************************

    $("#retrieve-btn").click(function () {

        let customer_id = $("#customer_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/customers/${customer_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });
    // ****************************************
    // Delete a Customer
    // ****************************************

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#customer_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Customer
    // ****************************************
    $("#search-btn").click(function () {
        let city = $("#customer_city").val();

        let queryString = ""

        if (city) {
            if (queryString.length > 0) {
                queryString += '&city=' + city
            } else {
                queryString += 'city=' + city
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/customers?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-1">ID</th>'
            table += '<th class="col-md-2">Firstname</th>'
            table += '<th class="col-md-2">Lastname</th>'
            table += '<th class="col-md-2">Email</th>'
            table += '<th class="col-md-2">Phone</th>'
            table += '<th class="col-md-2">Street_Line1</th>'
            table += '<th class="col-md-2">Street_Line2</th>'
            table += '<th class="col-md-2">City</th>'
            table += '<th class="col-md-2">State</th>'
            table += '<th class="col-md-2">Country</th>'
            table += '<th class="col-md-2">Zipcode</th>'
            table += '</tr></thead><tbody>'
            let firstCustomer = "";
            for(let i = 0; i < res.length; i++) {
                let customer = res[i];
                table +=  `<tr id="row_${i}">
                          <td>${customer.id}</td>
                          <td>${customer.firstname}</td>
                          <td>${customer.lastname}</td>
                          <td>${customer.email}</td>
                          <td>${customer.phone}</td>
                          <td>${customer.street_line1}</td>
                          <td>${customer.street_line2}</td>
                          <td>${customer.city}</td>
                          <td>${customer.state}</td>
                          <td>${customer.country}</td>
                          <td>${customer.zipcode}</td></tr>`;
                if (i == 0) {
                    firstCustomer = customer;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstCustomer != "") {
                update_form_data(firstCustomer)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
