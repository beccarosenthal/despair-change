// Chart.defaults.global.defaultFontFamily = "Lato";
// stackedOrgBarChart.canvas.parentnode.style.height = 200
Chart.defaults.global.defaultFontSize = 10;

// Chart.defaults.global = {

//     // Boolean - Determines whether to draw tooltips on the canvas or not
//     showTooltips: true,

//     // Array - Array of string names to attach tooltip events
//     tooltipEvents: ["mousemove", "touchstart", "touchmove"],

//     // String - Tooltip background colour
//     tooltipFillColor: "rgba(0,0,0,0.8)",

//     // String - Tooltip label font declaration for the scale label
//     tooltipFontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",

//     // Number - Tooltip label font size in pixels
//     tooltipFontSize: 14,

//     // String - Tooltip font weight style
//     tooltipFontStyle: "normal",

//     // String - Tooltip label font colour
//     tooltipFontColor: "#fff",

//     // String - Tooltip title font declaration for the scale label
//     tooltipTitleFontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",

//     // Number - Tooltip title font size in pixels
//     tooltipTitleFontSize: 14,

//     // String - Tooltip title font weight style
//     tooltipTitleFontStyle: "bold",

//     // String - Tooltip title font colour
//     tooltipTitleFontColor: "#fff",

//     // Number - pixel width of padding around tooltip text
//     tooltipYPadding: 6,

//     // Number - pixel width of padding around tooltip text
//     tooltipXPadding: 6,

//     // Number - Size of the caret on the tooltip
//     tooltipCaretSize: 8,

//     // Number - Pixel radius of the tooltip border
//     tooltipCornerRadius: 6,

//     // Number - Pixel offset from point x to tooltip edge
//     tooltipXOffset: 10,

//     // String - Template string for single tooltips
//     tooltipTemplate: "<%if (label){%><%=label%>: <%}%><%= value %>",

//     // String - Template string for single tooltips
//     multiTooltipTemplate: "<%= value %>",

//     // // Function - Will fire on animation progression.
//     // onAnimationProgress: function(){},

//     // // Function - Will fire on animation completion.
//     // onAnimationComplete: function(){}
// };

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
