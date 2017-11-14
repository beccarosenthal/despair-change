// // Demo talks about making json route to provide the data to the chart

"use strict";

var donut_options = { responsive: true };

var ctx_donut = $("#userImpactDonutChart").get(0).getContext("2d");

$.get("/user-impact-donut.json", function (data) {
    // console.log(data);
    var myDonutChart = new Chart(ctx_donut, {
                                            type: 'doughnut',
                                            data: data,
                                            options: donut_options
                                          });
    $('#donutLegend').html(myDonutChart.generateLegend());
});



var options = {
               responsive: true,
               barValueSpacing: 2,

               legend: {
                   display: true,
                   position: 'top',
                   labels: {
                        boxWidth: 80,
                        fontColor: 'black'
                    }
                  },

                scales: {
                    xAxes: [{
                      barThickness: 25,
                      barPercentage: 0.5,
                      gridLines: {
                        display: false,
                        color: "black"
                      },
                      ticks: {
                        autoSkip: false,
                        beginAtZero: true
                            },

                      scaleLabel: {
                        display: true,
                        labelString: "Organization",
                        fontColor: "name",
                        fontSize: 14
                      }
                    }],
                    yAxes: [{
                      gridLines: {
                        color: "black",
                        borderDash: [1, 5],
                      },
                      scaleLabel: {
                        display: true,
                        labelString: "Dollars Donated",
                        fontColor: "black"
                      },
                      ticks: { beginAtZero: true }
                    }],
                title: {
                    display: true,
                    text: 'My Donations',
                    fontSize: 24,
                    fontStyle: 'bold'
                       },
                layout: {
                    padding: {
                        left: 50,
                        right: 0,
                        top: 0,
                        bottom: 0
                    }}

                }};

var ctx_bar = $("#userImpactBarChart").get(0).getContext("2d");

$.get('/user-impact-bar.json', function (data) {
    console.log(data);
    var myBarChart = new Chart(ctx_bar, {
                                            type: 'bar',
                                            data: data,
                                            options: options
                                          });
    $('#barLegend').html(myBarChart.generateLegend());
});

//all users impact
// var ctx_total_bar = $("#totalImpactBarChart").get(0).getContext("2d");

// $.get('/total-impact-bar.json', function (data) {
//     console.log(data);
//     var totalBarChart = new Chart(ctx_total_bar, {
//                                             type: 'bar',
//                                             data: data,
//                                             options: options
//                                           });
//     $('#totalBarLegend').html(totalBarChart.generateLegend());
// });
