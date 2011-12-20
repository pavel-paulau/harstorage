"use strict";

/*
 * Name space
 */
var HARSTORAGE = HARSTORAGE || {};

/*
 * Dark green theme for Highcharts
 */
Highcharts.darkGreen = {
	colors: [
            '#DDDF0D',
            '#55BF3B',
            '#DF5353',
            '#7798BF',
            '#6AF9C4',
            '#DB843D',
            '#EEAAEE'
        ],
	chart: {
		backgroundColor: {
			linearGradient: [0, 0, 0, 500],
			stops: [
				[0, '#498A2D'],
				[1, '#000000']
			]
		},
		borderWidth: 0,
		plotBackgroundColor: 'rgba(255, 255, 255, .1)',
		plotBorderColor: '#CCCCCC',
		plotBorderWidth: 1
	},
	title: {
		style: {
			color       : '#FFFFFF',
                        fontWeight  : 'bold',
                        font        : 'bold 16px "Trebuchet MS", Verdana, sans-serif'
		}
	},
	xAxis: {
		gridLineColor: '#333333',
		gridLineWidth: 1,
                lineWidth: 0,
		labels: {
			style: {
				color: '#FFFFFF',
                                font: '11px "Trebuchet MS", Verdana, sans-serif'
			}
		},
		lineColor: '#FFFFFF',
		tickColor: '#FFFFFF'		
	},
	yAxis: {
		gridLineColor: '#333333',
		labels: {
			style: {
				color: '#FFFFFF',
                                font: '11px "Trebuchet MS", Verdana, sans-serif'
			}
		},
		lineColor: '#FFFFFF',
		minorTickInterval: null,
		tickColor: '#FFFFFF',
		tickWidth: 1,
		title: {
			style: {
				color: 'white',
                                font: 'bold 12px "Trebuchet MS", Verdana, sans-serif'                                
			}
		}
	},
	tooltip: {
		backgroundColor: 'rgba(0, 0, 0, 0.75)',
		style: {
			color: '#F0F0F0'
		}
	},
        toolbar: {
		itemStyle: {
			color: 'silver'
		}
	},
	plotOptions: {
		spline: {
			marker: {
				lineColor: '#333333'
			}
		},
                pie: {
                    allowPointSelect    : true,
                    cursor              : 'pointer',
                    size                : '65%',
                    dataLabels: {
                        enabled         : true,
                        color           : '#FFFFFF',
                        distance        : 25,
                        connectorColor  : '#FFFFFF',
                        formatter: function() {
                            return this.point.name;
                        }
                    }
                },
                column: {
                    pointPadding: 0.1,
                    borderWidth: 0,
                    borderColor: 'white',
                    dataLabels: {
                        enabled: true,
                        color: 'white',
                        align: 'left',
                        y: -5
                    }
                }
	},
	legend: {
		itemStyle: {
			font: '9pt "Trebuchet MS", Verdana, sans-serif',
			color: '#FFFFFF'
		},
		itemHoverStyle: {
			color: '#A0A0A0'
		},
		itemHiddenStyle: {
			color: '#444444'
		},
                borderColor: '#FFFFFF'
	}
};

/*
 * Light theme for Highcharts
 */
Highcharts.light = {
        colors: [
            '#669933',
            '#CC3333',
            '#FF9933',
            '#996633',
            '#4572A7',
            '#80699B',
            '#92A8CD',
            '#A47D7C'
        ],
	chart: {
		borderWidth: 1,
		borderColor: '#498A2D',
                plotBorderWidth: 1,
                plotBorderColor: '#498A2D'
	},
	title: {
		style: {
			color: '#498A2D',
                        fontWeight  : 'bold',
			font: 'bold 16px "Trebuchet MS", Verdana, sans-serif'
		}
	},
	xAxis: {
		gridLineWidth: 1,
		lineColor: '#498A2D',
		tickColor: '#498A2D',
                lineWidth: 0,
		labels: {
			style: {
				color: '#498A2D',
				font: '11px "Trebuchet MS", Verdana, sans-serif'
			}
		}
	},
	yAxis: {
                gridLineWidth: 1,
		lineColor: '#498A2D',
		tickColor: '#498A2D',
                tickWidth: 1,
		labels: {
			style: {
				color: '#498A2D',
				font: '11px "Trebuchet MS", Verdana, sans-serif'
			}
		},
		title: {
			style: {
                                font: 'bold 12px "Trebuchet MS", Verdana, sans-serif'
			}
		}
	},
        toolbar: {
		itemStyle: {
			color: 'silver'
		}
	},
        plotOptions: {
		spline: {
			marker: {
				lineColor: '#FFFFFF'
			}
		},
                pie: {
                    allowPointSelect    : true,
                    cursor              : 'pointer',
                    size                : '65%',
                    dataLabels: {
                        enabled         : true,
                        distance        : 25,
                        connectorColor  : '#498A2D',
                        color           : '#498A2D',
                        formatter: function() {
                            return this.point.name;
                        }
                    }
                },
                column: {
                    pointPadding: 0.1,
                    borderWidth: 0,
                    borderColor: 'white',
                    dataLabels: {
                        enabled: true,
                        color: '#498A2D',
                        align: 'left',
                        y: -5
                    }
                }
	},
        legend: {
		itemStyle: {
			font: '9pt "Trebuchet MS", Verdana, sans-serif',
			color: '#498A2D'

		},
		itemHoverStyle: {
			color: '#A0A0A0'
		},
		itemHiddenStyle: {
			color: 'gray'
		},
                borderWidth: 1,
		borderColor: '#498A2D'
	}
};

/*
 * Light green theme for Highcharts
 */
Highcharts.lightGreen = {
        colors: [
            '#669933',
            '#CC3333',
            '#FF9933',
            '#996633',
            '#4572A7',
            '#80699B',
            '#92A8CD',
            '#A47D7C'
        ],
	chart: {
		backgroundColor: {
			linearGradient: [0, 0, 0, 500],
			stops: [
				[0, '#F2FBED'],
				[1, '#99CC66']
			]
		},
		borderWidth: 1,
		borderColor: '#498A2D',
		plotBackgroundColor: 'rgba(255, 255, 255, .9)',
		plotBorderWidth: 0
	},
	title: {
		style: {
			color: '#498A2D',
                        fontWeight  : 'bold',
			font: 'bold 16px "Trebuchet MS", Verdana, sans-serif'
		}
	},
	xAxis: {
		gridLineWidth: 1,
		lineColor: '#498A2D',
		tickColor: '#498A2D',
                lineWidth: 0,
		labels: {
			style: {
				color: '#498A2D',
				font: '11px "Trebuchet MS", Verdana, sans-serif'
			}
		}
	},
	yAxis: {
                gridLineWidth: 1,
		lineColor: '#498A2D',
		tickColor: '#498A2D',
                tickWidth: 1,
		labels: {
			style: {
                                color: '#498A2D',
				font: '11px "Trebuchet MS", Verdana, sans-serif'
			}
		},
		title: {
			style: {
                                font: 'bold 12px "Trebuchet MS", Verdana, sans-serif'
			}
		}
	},
        toolbar: {
		itemStyle: {
			color: 'silver'
		}
	},
        plotOptions: {
		spline: {
			marker: {
				lineColor: '#FFFFFF'
			}
		},
                pie: {
                    allowPointSelect    : true,
                    cursor              : 'pointer',
                    size                : '65%',
                    dataLabels: {
                        enabled         : true,                        
                        distance        : 25,
                        connectorColor  : '#498A2D',
                        color           : '#498A2D',
                        formatter: function() {
                            return this.point.name;
                        }
                    }
                },
                column: {
                    pointPadding: 0.1,
                    borderWidth: 0,
                    borderColor: 'white',
                    dataLabels: {
                        enabled: true,
                        color: '#498A2D',
                        align: 'left',
                        y: -5
                    }
                }
	},
	legend: {
		itemStyle: {
			font: '9pt "Trebuchet MS", Verdana, sans-serif',
			color: '#498A2D'

		},
		itemHoverStyle: {
			color: '#000000'
		},
		itemHiddenStyle: {
			color: 'gray'
		},
                borderWidth: 1,
		borderColor: '#498A2D'
	}
};

/*
 * Theme setup
 */
HARSTORAGE.setTheme = function() {
    // Read preference from Cookie
    var theme = HARSTORAGE.read_cookie('chartTheme');

    if (theme) {
        switch (theme) {
        case "light":
            Highcharts.setOptions(Highcharts.light);
            break;
        case "light-green":
            Highcharts.setOptions(Highcharts.lightGreen);
            break;
        default:
            Highcharts.setOptions(Highcharts.darkGreen);
        }
    } else {
        Highcharts.setOptions(Highcharts.darkGreen);
    }
};

HARSTORAGE.setTheme();