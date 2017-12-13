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
              tooltips: tooltipDollarSignXAxis,
              legend: {
                       display: false,
                       labels: {
                                display: true,
                               }
                      },
              scales: {
                       xAxes: [
                              {gridLines: {
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
    var totalBarChart = new Chart(ctx_total_bar, {
                                            type: 'horizontalBar',
                                            data: data,
                                            options: options
                                          });
    // $('#totalBarLegend').html(totalBarChart.generateLegend());
});

