// // Demo talks about making json route to provide the data to the chart

"use strict";

var donut_options = { responsive: true };

var ctx_donut = $("#userImpactDonutChart").get(0).getContext("2d");

$.get("/user-impact-donut.json", function (data) {
    var myDonutChart = new Chart(ctx_donut, {
                                            type: 'doughnut',
                                            data: data,
                                            options: donut_options
                                          });
    $('#donutLegend').html(myDonutChart.generateLegend());
});



var options = {
               responsive: true,
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
                      gridLines: {
                        display: false,
                        color: "black"
                      },
                      scaleLabel: {
                        display: true,
                        labelString: "Organization",
                        fontColor: "red"
                      }
                    }],
                    yAxes: [{
                      gridLines: {
                        color: "black",
                        borderDash: [2, 5],
                      },
                      scaleLabel: {
                        display: true,
                        labelString: "Dollars Donated",
                        fontColor: "green"
                      }
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
    var myBarChart = new Chart(ctx_bar, {
                                            type: 'bar',
                                            data: data,
                                            options: options
                                          });
    $('#barLegend').html(myBarChart.generateLegend());
});
