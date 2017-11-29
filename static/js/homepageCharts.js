"use strict";

// Chart.defaults.global.defaultFontFamily = "Lato";
Chart.defaults.global.defaultFontSize = 18;
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
var options = {
                responsive: true,
               // barValueSpacing: 2,

               legend: {
                   display: true,
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
    $('#totalBarLegend').html(totalBarChart.generateLegend());
});


"use strict";
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
    $('#totalLineLegend').html(totalLineChart.generateLegend());
});


var ctx_org_bar = $("#stackedOrgBarChart").get(0).getContext("2d");

$.get('/stacked-org-bar.json', function (data) {
    console.log(data);
    console.log("stacked org bar function");
    var stackedOrgBarChart = new Chart(ctx_org_bar, {
                                            type: 'horizontalBar',
                                            data: data,
                                            options: stackedOptions
                                          });
    $('#stackedOrgBarLegend').html(stackedOrgBarChart.generateLegend());
});


