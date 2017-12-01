"use strict";

var numDonations;
var totalDonated;
var stackedBarState = 'totalDonated';
var currentChart;
var yAxisLabel = "Amount Donated";
var dollarSign = function(value, index, values) {
                          return value.toLocaleString("en-US",{style:"currency",
                                                              currency:"USD"});
                        };
var tooltipDollarSignXAxis = {
                enabled: true,
                mode: 'single',
                callbacks: {
                    label: function(tooltipItems, data) {
                        return '$' + tooltipItems.xLabel + '.00';
                    }
                }
            };

var tooltipDollarSignYAxis = {
                enabled: true,
                mode: 'single',
                callbacks: {
                    label: function(tooltipItems, data) {
                        return '$' + tooltipItems.yLabel + '.00';
                    }
                }
            };

var stackedOptions = {
                responsive: true,
               // barValueSpacing: 2,

               legend: {
                   display: true,
                   position: 'top',
                   labels: {
                        display: true,
                        boxWidth: 10,
                        fontColor: '#000000'
                    }
                  },
                // title: {
                //   display: true,
                //   text: "Your Impact"
                // },
                tooltips: tooltipDollarSignYAxis,
                scales: {
                    xAxes: [{
                      // barThickness: 50,
                      stacked: true,
                      barPercentage: 0.5,
                      gridLines: {
                        display: false,
                        color: "grey"
                      },
                      ticks: {
                        autoSkip: true,
                        beginAtZero: true,
                        // callback: function(value, index, values) {
                        //   return value.toLocaleString("en-US",{style:"currency",
                        //                                       currency:"USD"});
                            // },

                      scaleLabel: {
                        display: true,
                        labelString: "Date",
                        fontColor: "black",
                        // fontSize: 14
                      }
                    }}],
                    yAxes: [{
                      stacked: true,
                      gridLines: {
                        color: "grey",
                      },
                      scaleLabel: {
                        display: true,
                        labelString: yAxisLabel,
                        fontColor: "black"
                      },
                      ticks: {
                        beginAtZero: true,
                        // stepSize: 5,
                        // if stackedBarState
                        callback: dollarSign,
                        // callback: function(value, index, values) {
                        //   return value.toLocaleString("en-US",{style:"currency",
                        //                                      currency:"USD"});
                        // }
                    }
                  }],
                title: {
                    display: false,
                    text: 'I\'m the Title',
                    fontSize: 24,
                    fontStyle: 'bold',

                       },

                }};
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


var lineOptions = {
                responsive: true,}
               // barValueSpacing: 2,

               // legend: {
               //     display: true,
               // //     position: 'top',
               //     labels: {
               //          display: true,
               // //          boxWidth: 80,
               // //          fontColor: '#000080'
               //      }
               //    },
               // //  // title: {
               // //  //   display: true,
               // //  //   text: "Your Impact"
               // //  // },

               //  scales: {
               //      xAxes: [
               //      {
               // //        // barThickness: 50,
               // //        barPercentage: 0.5,
               //        gridLines: {
               //          display: false,
               //          color: "grey"
               //        },
               // //        ticks: {
               // // //          autoSkip: true,
               // //          beginAtZero: true,
               // //            callback: function(value, index, values) {
               // //            return value.toLocaleString("en-US",{style:"currency",
               // //                                                currency:"USD"});
               // //              },

               // // //        scaleLabel: {
               // // //          display: true,
               // // //          labelString: "Organization",
               // // //          fontColor: "black",
               // // //          // padding: 14
               // //        }
               //      }],
               // //      yAxes: [{
               // //        gridLines: {
               // //          color: "grey",
               // //        },
               // //        scaleLabel: {
               // //          display: true,
               // //          labelString: "Dollars Donated",
               // //          fontColor: "black"
               // //        },
               // //        ticks: {
               // //          beginAtZero: true,
               // //          stepSize: 5,
               // //          callback: function(value, index, values) {
               // //            return value.toLocaleString("en-US",{style:"currency",
               // //                                               currency:"USD"});
               //          }
               //      }
               //    }],
               //  title: {
               //      display: true,
               //      text: 'My Donations',
               //      fontSize: 24,
               //      fontStyle: 'bold'
              //  //         },

              //   // }
              // };

var ctx = document.getElementById("datetimeTotalLineChart").getContext('2d');

// $.get('/total-impact-bar.json', function (data) {
$.get('/donations-over-time-line.json', function (data) {
    console.log(data);
    console.log("line  function");
    var totalLineChart = new Chart(ctx, {
                                            type: 'line',
                                            data: data,
                                            options: lineOptions
                                          });
    // $('#totalLineLegend').html(totalLineChart.generateLegend());
});


var ctx_org_bar = $("#stackedOrgBarChart").get(0).getContext("2d");
function renderStackedBar(data) {
    console.log(data);
    console.log("renderStackedBar function");

    var stackedOrgBarChart = new Chart(ctx_org_bar, {
                                            type: 'bar',
                                            data: data,
                                            options: stackedOptions,
                                          });
    currentChart = stackedOrgBarChart;
    // $('#stackedOrgBarLegend').html(stackedOrgBarChart.generateLegend());
}

$.get('/stacked-org-bar.json', function (data) {
    console.log(data);

    totalDonated = data['total_donated'];
    numDonations = data['num_donations'];
    renderStackedBar(totalDonated);

});
// function to toggle the chart
function toggleStackedBar() {
  currentChart.destroy()
  if (stackedBarState == 'totalDonated') {
    $('#num-donations').show();
    $('#total-donated').hide();
      stackedOptions.scales.yAxes[0].scaleLabel.labelString = "Number of Donations";
      delete stackedOptions.scales.yAxes[0].ticks.callback;
      delete stackedOptions.tooltips.callbacks;
      renderStackedBar(numDonations);
      stackedBarState = 'numDonations';

  } else {
    $('#total-donated').show();
    $('#num-donations').hide();
      stackedOptions.scales.yAxes[0].scaleLabel.labelString = "Amount Donated";
      stackedOptions.scales.yAxes[0].ticks.callback = dollarSign;
      stackedOptions.tooltips = tooltipDollarSignYAxis;
      renderStackedBar(totalDonated);
      stackedBarState = 'totalDonated';
  }

}

// for search bars above tables
$(document).ready(function(){
  $('#num-donations').hide();
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    console.log("in searching filter table function");
    $("#transactionTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
});
