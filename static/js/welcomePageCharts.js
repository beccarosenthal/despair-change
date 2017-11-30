"use strict";


$('#edit').on('hidden.bs.modal', function() {
    location.reload();
});

/* must apply only after HTML has loaded */
$(document).ready(function() {
    $("#updateForm").on("submit", function(e) {

        $(".error").hide();
        var hasError = false;
        // var currentpass = $("#current_pass").val();
        var newpass = $("#new_pass").val();
        var cnfpass = $("#confirm_pass").val();

        // if (currentpass == '') {
        //     $("#current_pass").after('<span class="error text-danger"><em>Please  enter your current password.</em></span>');
            //$('#currentPass-group').addClass('has-error'); // add the error class to show red input
            // //$('#current_pass').append('<div class="help-block">Please enter your current password.</div>'); // add the actual error message under our input
            // hasError = true;
        } else if (newpass == '') {
            $("#new_pass").after('<span class="error text-danger"><em>Please enter a password.</em></span>');
            hasError = true;
        } else if (cnfpass == '') {
            $("#confirm_pass").after('<span class="error text-danger"><em>Please re-enter your password.</em></span>');
            hasError = true;
        } else if (newpass != cnfpass) {
            $("#confirm_pass").after('<span class="error text-danger"><em>Passwords do not match.</em></span>');
            hasError = true;
        }

        if (hasError == true) {
            return false;
        }
        if (hasError == false) {

            var postData = $(this).serializeArray();
            var formURL = $(this).attr("action");
            $.ajax({
                url: formURL,
                type: "POST",
                data: postData,
                success: function(data, textStatus, jqXHR) {
                    $('#edit .modal-header .modal-title').html("Result");
                    $('#edit .modal-body').html(data);
                    $("#submitForm").remove();
                    //document.location.reload();
                },
                error: function(jqXHR, status, error) {
                    console.log(status + ": " + error);
                }
            });
            e.preventDefault();
        }
    });

    $("#submitForm").on('click', function() {
        $("#updateForm").submit();
    });
});
