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
        $("#customer_name").val("");
        $("#customer_category").val("");
        $("#customer_available").val("");
        $("#customer_gender").val("");
        $("#customer_birthday").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Customer
    // ****************************************

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

})
