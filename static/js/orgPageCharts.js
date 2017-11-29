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

// var ctx_stacked_bar = $("#stackedUserImpactBarChart").get(0).getContext("2d");

// $.get('/stacked-user-impact-bar.json', function (data) {
//     console.log(data);
//     console.log("stacked impact bar function");
//     var stackedBarChart = new Chart(ctx_stacked_bar, {
//                                             type: 'horizontalBar',
//                                             data: data,
//                                             options: stackedOptions
//                                           });
//     $('#stackedBarLegend').html(stackedBarChart.generateLegend());
// });
