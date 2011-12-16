"use strict";

/*
 * Name space
 */
var HARSTORAGE = HARSTORAGE || {};

/*
 * Dark green theme for Highcharts
 */
Highcharts.dark_green = {
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
				[0, 'rgb(73, 138, 45)'],
				[1, 'rgb(0, 0, 0)']
			]
		},
		borderWidth: 0,
		plotBackgroundColor: 'rgba(255, 255, 255, .1)',
		plotBorderColor: '#CCCCCC',
		plotBorderWidth: 1
	},
	title: {
		style: {
			color       : '#ffffff',
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
                        color           : '#FFF',
                        distance        : 25,
                        connectorColor  : '#FFF',                        
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
            '#89A54E',
            '#DF5353',
            '#DB843D',
            '#3D96AE',
            '#4572A7',
            '#80699B',
            '#92A8CD',
            '#A47D7C'
        ],
	chart: {
		borderWidth: 1,
		borderColor: '#498a2d',
                plotBorderWidth: 1,
                plotBorderColor: '#498a2d'
	},
	title: {
		style: {
			color: '#498a2d',
                        fontWeight  : 'bold',
			font: 'bold 16px "Trebuchet MS", Verdana, sans-serif'
		}
	},
	xAxis: {
		gridLineWidth: 1,
		lineColor: '#498a2d',
		tickColor: '#498a2d',
                lineWidth: 0,
		labels: {
			style: {
				color: '#498a2d',
				font: '11px "Trebuchet MS", Verdana, sans-serif'
			}
		}
	},
	yAxis: {
                gridLineWidth: 1,
		lineColor: '#498a2d',
		tickColor: '#498a2d',
                tickWidth: 1,
		labels: {
			style: {
				color: '#498a2d',
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
                        connectorColor  : '#498a2d',
                        color           : '#498a2d',
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
                        color: '#498a2d',
                        align: 'left',
                        y: -5
                    }
                }
	},
        legend: {
		itemStyle: {
			font: '9pt "Trebuchet MS", Verdana, sans-serif',
			color: '#498a2d'

		},
		itemHoverStyle: {
			color: '#A0A0A0'
		},
		itemHiddenStyle: {
			color: 'gray'
		},
                borderWidth: 1,
		borderColor: '#498a2d'
	}
};

/*
 * Light green theme for Highcharts
 */

Highcharts.light_green = {
        colors: [
            '#89A54E',            
            '#DF5353',
            '#DB843D',
            '#3D96AE',
            '#4572A7',
            '#80699B',
            '#92A8CD',
            '#A47D7C'
        ],
	chart: {
		backgroundColor: {
			linearGradient: [0, 0, 0, 500],
			stops: [
				[0, '#f2fbed'],
				[1, '#c0d0b8']
			]
		},
		borderWidth: 1,
		borderColor: '#498a2d',
		plotBackgroundColor: 'rgba(255, 255, 255, .9)',
		plotBorderWidth: 0
	},
	title: {
		style: {
			color: '#498a2d',
                        fontWeight  : 'bold',
			font: 'bold 16px "Trebuchet MS", Verdana, sans-serif'
		}
	},
	xAxis: {
		gridLineWidth: 1,
		lineColor: '#498a2d',
		tickColor: '#498a2d',
                lineWidth: 0,
		labels: {
			style: {
				color: '#498a2d',
				font: '11px "Trebuchet MS", Verdana, sans-serif'
			}
		}
	},
	yAxis: {
                gridLineWidth: 1,
		lineColor: '#498a2d',
		tickColor: '#498a2d',
                tickWidth: 1,
		labels: {
			style: {
                                color: '#498a2d',
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
                        connectorColor  : '#498a2d',
                        color           : '#498a2d',
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
                        color: '#498a2d',
                        align: 'left',
                        y: -5
                    }
                }
	},
	legend: {
		itemStyle: {
			font: '9pt "Trebuchet MS", Verdana, sans-serif',
			color: '#498a2d'

		},
		itemHoverStyle: {
			color: '#000000'
		},
		itemHiddenStyle: {
			color: 'gray'
		},
                borderWidth: 1,
		borderColor: '#498a2d'                
	}
};

HARSTORAGE.setTheme = function() {
    // Read preference from Cookie
    var theme = HARSTORAGE.read_cookie('chartTheme');

    if (theme) {
        switch (theme) {
        case "light":
            Highcharts.setOptions(Highcharts.light);
            break;
        case "light-green":
            Highcharts.setOptions(Highcharts.light_green);
            break;
        default:
            Highcharts.setOptions(Highcharts.dark_green);            
        }
    } else {
        Highcharts.setOptions(Highcharts.dark_green);        
    }
};

HARSTORAGE.setTheme();