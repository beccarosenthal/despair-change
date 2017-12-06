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

