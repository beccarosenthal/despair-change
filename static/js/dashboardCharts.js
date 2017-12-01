"use strict";

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

var donutOptions = { responsive: true,
               legend: {
                   display: true,
                   position: 'left',
                   labels: {
                        display: true,
                        boxWidth: 10,
                        // fontColor: '#000000'
                    }
                  },
                }
var options = {
                responsive: true,
               // barValueSpacing: 2,
               tooltips: tooltipDollarSignYAxis,
               legend: {
                   display: true,
                   position: 'top',
                   labels: {
                        display: true,
                        boxWidth: 80,
                        fontColor: '#000000'
                    }
                  },
                // title: {
                //   display: true,
                //   text: "Your Impact"
                // },

                scales: {
                    xAxes: [{
                      // barThickness: 50,
                      barPercentage: 0.5,
                      gridLines: {
                        display: false,
                        color: "grey"
                      },
                      ticks: {
                        autoSkip: true,
                        beginAtZero: true,
                        callback: function(value, index, values) {
                          return value.toLocaleString("en-US",{style:"currency",
                                                              currency:"USD"});
                            },

                      scaleLabel: {
                        display: true,
                        labelString: "Organization",
                        fontColor: "black",

                        // fontSize: 14
                      }
                    }}],
                    yAxes: [{
                      gridLines: {
                        color: "grey",
                      },
                      scaleLabel: {
                        display: true,
                        labelString: "Dollars Donated",
                        fontColor: "black"
                      },
                      ticks: {
                        beginAtZero: true,
                        stepSize: 5,
                        callback: function(value, index, values) {
                          return value.toLocaleString("en-US",{style:"currency",
                                                             currency:"USD"});
                        }
                    }
                  }],
                title: {
                    display: true,
                    text: 'My Donations',
                    fontSize: 24,
                    fontStyle: 'bold'
                       },

                }};

var ctx_bar = $("#userImpactBarChart").get(0).getContext("2d");

$.get('/user-impact-bar.json', function (data) {
    console.log(data);
    console.log("user impact bar function");
    var myBarChart = new Chart(ctx_bar, {
                                            type: 'bar',
                                            data: data,
                                            options: options
                                          });
    $('#barLegend').html(myBarChart.generateLegend());
});

var ctx_donut = $("#userImpactDonutChart").get(0).getContext("2d");

$.get('/user-impact-donut.json', function (data) {
    console.log(data);
    console.log("user impact donut function");
    var myDonutChart = new Chart(ctx_donut, {
                                            type: 'doughnut',
                                            data: data,
                                            options: donutOptions
                                          });
    // $('#donutLegend').html(myDonutChart.generateLegend());
});

var stackedOptions = {
                responsive: true,
               // barValueSpacing: 2,

               legend: {
                   display: true,
                   position: 'top',
                   labels: {
                        display: true,
                        boxWidth: 40,
                        fontColor: '#000000'
                    }
                  },
                // title: {
                //   display: true,
                //   text: "Your Impact"
                // },
                tooltips: tooltipDollarSignXAxis,
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
                        callback: function(value, index, values) {
                          return value.toLocaleString("en-US",{style:"currency",
                                                              currency:"USD"});
                            },

                      scaleLabel: {
                        display: true,
                        labelString: "Organization",
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
                        labelString: "Dollars Donated",
                        fontColor: "black"
                      },
                      ticks: {
                        beginAtZero: true,
                        stepSize: 5,
                        callback: function(value, index, values) {
                          return value.toLocaleString("en-US",{style:"currency",
                                                             currency:"USD"});
                        }
                    }
                  }],
                title: {
                    display: false,
                    text: 'I\'m the Title',
                    fontSize: 24,
                    fontStyle: 'bold',

                       },

                }};

var ctx_stacked_bar = $("#stackedUserImpactBarChart").get(0).getContext("2d");

$.get('/stacked-user-impact-bar.json', function (data) {
    console.log(data);
    console.log("stacked impact bar function");
    var stackedBarChart = new Chart(ctx_stacked_bar, {
                                            type: 'horizontalBar',
                                            data: data,
                                            options: stackedOptions
                                          });
    $('#stackedBarLegend').html(stackedBarChart.generateLegend());
});


// To play with stuff live in console
let renderChart = ()=> {
  let testData = {'labels': ['Institute of Finishi',
  'Rent-A-Swag', 'Alternative US Natio',
  'The Derek Zoolander ',
   'Alt ACLU'],
   'datasets': [{'hoverBackgroundColor': '#FF6384',
   'data': [4.0, 5.0, 2.0, 3.0, 4.0], 'backgroundColor': '#C72DB3',
   'label': ['My Donations']}, {'hoverBackgroundColor': '#D9A622',
   'data': [9.0, 12.0, 13.0, 2.0, 20.0], 'backgroundColor': '#2DC7C0',
   'label': ['My Footprint']}]}

  let barChart = new Chart(ctx_stacked_bar, {
                                            type: 'bar',
                                            data: testData,
                                            options: stackedOptions
                                          });
    $('#totalBarLegend').html(barChart.generateLegend());};

