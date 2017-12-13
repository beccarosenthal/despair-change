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
                maintainAspectRatio: false,
                legend: {
                  display: true,
                  position: 'top',
                  labels: {
                      display: true,
                      boxWidth: 10,
                          }
                  },
                tooltips: tooltipDollarSignXAxis,
                tooltips: tooltipDollarSignYAxis,
                scales: {
                    xAxes: [{
                      stacked: true,
                      barPercentage: 0.5,
                      gridLines: {
                        display: false,
                        color: "grey"
                      },
                      ticks: {
                        autoSkip: true,
                        beginAtZero: true,

                      scaleLabel: {
                        display: true,
                        labelString: "Date",
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
                      },
                      ticks: {
                        beginAtZero: true,
                        callback: dollarSign,
                    }
                  }],
            

                }};
var options = {
               responsive: true,
               tooltips: tooltipDollarSignXAxis,
               legend: {
                   display: false,
                   labels: {
                        display: true,
                    }
                  },

                scales: {
                    xAxes: [
                    {
                      gridLines: {
                        display: false,
                        color: "grey"
                      },
                      ticks: {
                        beginAtZero: true,

                          callback: function(value, index, values) {
                          return value.toLocaleString("en-US",{style:"currency",
                                                              currency:"USD"});
                            },

                      }
                    }],
                        }

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

// Try to get $ to show up on tooltip https://codepen.io/mab213/pen/PZOXdE
var donutOptions = { responsive: true,
                    tooltipTemplate: "<%= value %>$",
                    onAnimationComplete: function() {
                      console.log('animation complete');
                    this.showTooltip(this.segments, true);
    },
               legend: {
                   display: true,
                   position: 'top',
                   labels: {
                        display: true,
                        boxWidth: 10,

                    }
                  },
                };


var current_user = $('#current-user-in-session').val();
console.log(current_user);

if (current_user != "false") {
var ctx_donut = $("#userImpactDonutChart").get(0).getContext("2d");
$.get('/user-impact-donut.json', function (data) {
    console.log(data);
    console.log("user impact donut function");
    var myDonutChart = new Chart(ctx_donut, {
                                            type: 'doughnut',
                                            data: data,
                                            options: donutOptions
                                          });
    $('#donutLegend').html(myDonutChart.generateLegend());
});
}



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
      delete stackedOptions.tooltips;
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
  // $('#donationModal').modal('show');
  $('#num-donations').hide();
  $("#myInput").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    console.log("in searching filter table function");
    $("#transactionTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
    });
  });
  


  });


var lineOptions = {
                responsive: true,
              maintainAspectRatio: false,}
               // barValueSpacing: 2,


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