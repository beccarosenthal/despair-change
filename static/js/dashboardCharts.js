"use strict";

var options = {
                responsive: true,
               // barValueSpacing: 2,

               legend: {
                   display: true,
                   position: 'top',
                   labels: {
                        display: true,
                        boxWidth: 80,
                        fontColor: '#000080'
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
                        autoSkip: false,
                        beginAtZero: true
                            },

                      scaleLabel: {
                        display: true,
                        labelString: "Organization",
                        fontColor: "black",
                        // fontSize: 14
                      }
                    }],
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
                        stepSize: 1,
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

var stackedOptions = {
                responsive: true,
               // barValueSpacing: 2,

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
                      stacked: true,
                      barPercentage: 0.5,
                      gridLines: {
                        display: false,
                        color: "grey"
                      },
                      ticks: {
                        autoSkip: false,
                        beginAtZero: true
                            },

                      scaleLabel: {
                        display: true,
                        labelString: "Organization",
                        fontColor: "black",
                        // fontSize: 14
                      }
                    }],
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
                        stepSize: 1,
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

var ctx_stacked_bar = $("#stackedUserImpactBarChart").get(0).getContext("2d");

$.get('/stacked-user-impact-bar.json', function (data) {
    console.log(data);
    console.log("stacked impact bar function");
    var stackedBarChart = new Chart(ctx_stacked_bar, {
                                            type: 'bar',
                                            data: data,
                                            options: stackedOptions
                                          });
    $('#stackedBarLegend').html(stackedBarChart.generateLegend());
});


