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
        // } else 
        if (newpass == '') {
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
var tooltipDollarSignXAxis = {
                enabled: true,
                mode: 'single',
                callbacks: {
                    label: function(tooltipItems, data) {
                        return '$' + tooltipItems.xLabel + '.00';
                    }
                }
            };
var options = {
                responsive: true,
               // barValueSpacing: 2,

               tooltips: tooltipDollarSignXAxis,
               legend: {
                   display: false,
               //     position: 'top',
                   labels: {
                        display: true,
               //          boxWidth: 80,
               //          fontColor: '#000080'
                    }
                  },
               //  // title: {
               //  //   display: true,
               //  //   text: "Your Impact"
               //  // },

                scales: {
                    xAxes: [
                    {
               //        // barThickness: 50,
               //        barPercentage: 0.5,
                      gridLines: {
                        display: false,
                        color: "grey"
                      },
                      ticks: {
               //          autoSkip: true,
                        beginAtZero: true,

                          callback: function(value, index, values) {
                          return value.toLocaleString("en-US",{style:"currency",
                                                              currency:"USD"});
                            },

               //        scaleLabel: {
               //          display: true,
               //          labelString: "Organization",
               //          fontColor: "black",
               //          // padding: 14
                      }
                    }],
               //      yAxes: [{
               //        gridLines: {
               //          color: "grey",
               //        },
               //        scaleLabel: {
               //          display: true,
               //          labelString: "Dollars Donated",
               //          fontColor: "black"
               //        },
               //        ticks: {
               //          beginAtZero: true,
               //          stepSize: 5,
               //          callback: function(value, index, values) {
               //            return value.toLocaleString("en-US",{style:"currency",
               //                                               currency:"USD"});
                        }
               //      }
               //    }],
               //  title: {
               //      display: true,
               //      text: 'My Donations',
               //      fontSize: 24,
               //      fontStyle: 'bold'
               //         },

                // }
              };

var ctx_total_bar = $("#totalImpactBarChart").get(0).getContext("2d");

$.get('/total-impact-bar.json', function (data) {
    console.log(data);
    console.log("total bar function");
    var totalBarChart = new Chart(ctx_total_bar, {
                                            type: 'horizontalBar',
                                            data: data,
                                            options: options
                                          });
    // $('#totalBarLegend').html(totalBarChart.generateLegend());
});
});
