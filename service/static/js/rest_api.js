$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_id").val(res.id);
        $("#pet_name").val(res.name);
        $("#pet_category").val(res.category);
        if (res.available == true) {
            $("#pet_available").val("true");
        } else {
            $("#pet_available").val("false");
        }
        $("#pet_gender").val(res.gender);
        $("#pet_birthday").val(res.birthday);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#pet_name").val("");
        $("#pet_category").val("");
        $("#pet_available").val("");
        $("#pet_gender").val("");
        $("#pet_birthday").val("");
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

})
