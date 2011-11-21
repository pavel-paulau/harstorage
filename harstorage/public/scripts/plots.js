"use strict";

/*
 * Timeline chart
 */
var Timeline = function() {};

// Get data for timeline
Timeline.prototype.get = function(url, label, mode) {
    // Retrieve data for timeline via XHR call
    var xmlhttp = new XMLHttpRequest();
    var that = this;

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            that.draw(xmlhttp.responseText);
        }
    };

    var URI = 'timeline?url=' + url + '&label=' + label + '&mode=' + mode;

    xmlhttp.open('GET', URI, true);
    xmlhttp.send();
};

// Draw timeline
Timeline.prototype.draw = function(points) {
    var splitResults = points.split(';');

    var tsArray     = splitResults[0].split('#'),
        timeArray   = splitResults[1].split('#'),
        sizeArray   = splitResults[2].split('#'),
        reqArray    = splitResults[3].split('#'),
        scoreArray  = splitResults[4].split('#');

    for (var index = 0, len = tsArray.length; index < len; index++) {
        timeArray[index]    =   parseFloat(timeArray[index], 10);
        sizeArray[index]    =   parseFloat(sizeArray[index], 10);
        reqArray[index]     =   parseInt(reqArray[index], 10);
        scoreArray[index]   =   parseInt(scoreArray[index], 10);
    }

    var chart = new Highcharts.Chart({
        chart: {
            renderTo    : 'timeline',
            zoomType    : 'x'
        },
        credits: {
            enabled: false
        },
        exporting: {
            buttons : {
                printButton : {
                    enabled: false
                },
                exportButton: {
                    menuItems: [
                        {},
                        null,
                        null,
                        {}
                    ]
                }
            },
            url         : '/chart/export',
            filename    : 'timeline',
            width       : 960            
        },
        title: {
            text: 'Performance Trends'
        },
        xAxis: [{
            categories          : tsArray,
            tickInterval        : Math.ceil(tsArray.length / 10),
            tickmarkPlacement   : 'on'
        }],
        yAxis: [{ // yAxis #1
            title: {
                text    : 'Full Load Time',
                style   : {color: '#DDDF0D'}
            },
            min         : 0,
            labels: {
                formatter: function() {
                    return this.value;
                }
            }
        }, { // yAxis #2
            title: {
                text    : 'Total Requests',
                style   : {color: '#55BF3B'}
            },
            min         : 0,
            opposite    : true
        }, { // yAxis #3
            title: {
                text    : 'Total Size (kB)',
                style   : {color: '#DF5353'}
            },
            min         : 0,
            opposite    : true,
            labels: {
                formatter: function() {
                    return this.value;
                }
            }
        }, { // yAxis #4
            title: {
                text    : 'Page Speed Score',
                style   : {color: '#7798BF'}
            },
            min         : 0            
        }],
        tooltip: {
            formatter: function() {
                var unit = {
                    'Full Load Time'    : 's',
                    'Total Requests'    : '',
                    'Total Size'        : 'kB',
                    'Page Speed Score'  : ''
                }[this.series.name];

                return '<b>' + this.y + ' ' + unit + '</b>' + ' (' + this.x + ')';
            }
        },
        plotOptions: {
            series: {
                cursor: 'pointer',
                events: {
                    hide: function() {
                        this.yAxis.axisTitle.hide();
                    },
                    show: function() {
                        this.yAxis.axisTitle.show();
                    }
                },
                point: {
                    events: {
                        click: function() {
                            run_info.get(this.category);
                        }
                    }
                }
            }
        },
        series: [{
            name    : 'Full Load Time',
            type    : 'spline',
            yAxis   : 0,
            data    : timeArray
        }, {
            name    : 'Total Requests',
            type    : 'spline',
            yAxis   : 1,
            data    : reqArray
        }, {
            name    : 'Total Size',
            type    : 'spline',
            yAxis   : 2,
            data    : sizeArray
        }, {
            name    : 'Page Speed Score',
            type    : 'spline',
            yAxis   : 3,
            data    : scoreArray
        } ]
    });
};

/*
 * Column Chart
 */
var Column = function() {};

Column.prototype.draw = function(points) {
    var splitResults = points.split(';');

    var tsArray     = splitResults[0].split('#'),
        timeArray   = splitResults[1].split('#'),
        sizeArray   = splitResults[2].split('#'),
        reqArray    = splitResults[3].split('#'),
        scoreArray  = splitResults[4].split('#');

    for (var index = 0, len = tsArray.length; index < len; index++) {
        timeArray[index]    =   parseFloat(timeArray[index], 10);
        sizeArray[index]    =   parseFloat(sizeArray[index], 10);
        reqArray[index]     =   parseInt(reqArray[index], 10);
        scoreArray[index]   =   parseInt(scoreArray[index], 10);
    }

    var chart = new Highcharts.Chart({
        chart: {
            renderTo    : 'chart',
            defaultSeriesType: 'column'
        },
        credits: {
            enabled: false
        },
        exporting: {
            buttons : {
                printButton : {
                    enabled: false
                },
                exportButton: {
                    menuItems: [
                        {},
                        null,
                        null,
                        {}
                    ]
                }
            },
            url         : '/chart/export',
            filename    : 'superposed',
            width       : 960            
        },
        title: {
            text: 'Performance Trends'
        },
        xAxis: [{
            categories          : tsArray,
            tickInterval        : Math.ceil(tsArray.length / 10),
            tickmarkPlacement   : 'on'
        }],
        yAxis: [{ // yAxis #1
            title: {
                text    : 'Full Load Time',
                style   : {color: '#DDDF0D'}
            },
            min         : 0,
            labels: {
                formatter: function() {
                    return this.value;
                }
            }
        }, { // yAxis #2
            title: {
                text    : 'Total Requests',
                style   : {color: '#55BF3B'}
            },
            min         : 0,
            opposite    : true
        }, { // yAxis #3
            title: {
                text    : 'Total Size (kB)',
                style   : {color: '#DF5353'}
            },
            min         : 0,
            opposite    : true,
            labels: {
                formatter: function() {
                    return this.value;                    
                }
            }
        }, { // yAxis #4
            title: {
                text    : 'Page Speed Score',
                style   : {color: '#7798BF'}
            },
            min         : 0,
            endOnTick   : false
        }],
        tooltip: {
            formatter: function() {
                var unit = {
                    'Full Load Time'    : 's',
                    'Total Requests'    : '',
                    'Total Size'        : 'kB',
                    'Page Speed Score'  : ''
                }[this.series.name];

                return '<b>' + this.y + ' ' + unit + '</b>' + ' (' + this.x + ')';
            }
        },
        plotOptions: {
            series: {
                events: {
                    hide: function() {
                        this.yAxis.axisTitle.hide();
                    },
                    show: function() {
                        this.yAxis.axisTitle.show();
                    }
                }
            },
            column: {
                pointPadding: 0.1,
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    color: 'white',
                    align: 'left',
                    y: -5
                }
            }
        },
        series: [{
            name    : 'Full Load Time',
            yAxis   : 0,
            data    : timeArray
        }, {
            name    : 'Total Requests',            
            yAxis   : 1,
            data    : reqArray
        }, {
            name    : 'Total Size',            
            yAxis   : 2,
            data    : sizeArray
        }, {
            name    : 'Page Speed Score',            
            yAxis   : 3,
            data    : scoreArray
        }]
    });    
};

/*
 * Test results
 */
var RunInfo = function() {};

//Gauge chart
RunInfo.prototype.score = function(score) {
    // Value for chart
    var data = new google.visualization.DataTable();

    data.addColumn('string');
    data.addColumn('number');
    data.addRows(1);
    data.setValue(0, 0, 'PS Score');
    data.setValue(0, 1, score);

    // Chart options
    var options = {
        width       : 200,
        height      : 200,
        redFrom     : 0,
        redTo       : 59,
        yellowFrom  : 60,
        yellowTo    : 79,
        greenFrom   : 80,
        greenTo     : 100,
        minorTicks  : 10
    };

    // Chart object
    var chart = new google.visualization.Gauge( document.getElementById('gauge') );
    
    chart.draw(data, options);
};

//Page Resources
RunInfo.prototype.resources = function (div,title,hash,units) {
    // Extract data
    var data  = [];

    for (var key in hash) {
        data.push( [key, hash[key] ]);
    }

    // Chart object
    var chart = new Highcharts.Chart({
        chart: {
            renderTo            : div,
            plotBackgroundColor : null,
            plotBorderWidth     : null,
            plotShadow          : false,
            width               : 450,
            height              : 300
        },
        credits: {
            enabled: false
        },
        exporting: {
            buttons : {
                printButton: {
                    enabled: false
                },
                exportButton: {
                    menuItems: [
                        {},
                        null,
                        null,
                        {}
                    ]
                }
            },
            url         :'/chart/export',
            filename    : 'resources',
            width       : 450            
        },
        title: {
            text: title
        },
        tooltip: {
            formatter: function() {
                return '<b>'+ this.point.name +'</b>: '+ this.y + units;
            }
        },
        plotOptions: {
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
            series: {
                showInLegend: true
            }
        },
        series: [{
            type: 'pie',
            data: data    
        }]
    });
};

//Page Speed details
RunInfo.prototype.pagespeed = function (pagespeed) {
    // Spliting data for chart
    var rules   = [],
        scores  = [];

    for (var rule in pagespeed) {
        rules.push(rule);
        scores.push(pagespeed[rule]);
    }

    // Chart height
    var height = Math.max(75 + 20 * rules.length, 100);

    // Chart object
    var chart = new Highcharts.Chart({
        chart: {
            renderTo            : 'pagespeed',
            defaultSeriesType   : 'bar',
            height              : height,
            width               : 930
        },
        credits: {
            enabled: false
        },
        exporting: {
            buttons : {
                printButton: {
                    enabled: false
                },
                exportButton: {
                    enabled: false
                }
            }
        },
        title: {
            text: 'Page Speed Scores'
        },
        xAxis: {
            title: {
                text: null
            },
            categories  : rules
        },
        yAxis: {
            title: {
                text: null
            },
            min         : 0,
            max         : 105,
            endOnTick   : false

        },
        tooltip: {
            formatter: function() {
                return this.x +': '+ this.y;
            }
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled     : true
                }
            },
            series: {
                showInLegend    : false,
                animation       : false
            }
        },
        series: [{
            data: scores
        }]
    });
};

//Get data for Run Info
RunInfo.prototype.get = function(opt_ts) {
    // Retrieve data for Run Infor via XHR call
    var xmlhttp = new XMLHttpRequest();

    var that = this;

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            var json = JSON.parse(xmlhttp.responseText);
            
            // Summary
            $('#full-load-time').html(json.summary.full_time+' ms');
            $('#dns').html(json.summary.dns+' ms');
            $('#transfer').html(json.summary.transfer+' ms');
            $('#connecting').html(json.summary.connecting+' ms');
            $('#server').html(json.summary.server+' ms');
            $('#blocked').html(json.summary.blocked+' ms');
            
            $('#total-size').html(json.summary.total_size+' kB');
            $('#text-size').html(json.summary.text_size+' kB');
            $('#media-size').html(json.summary.media_size+' kB');
            $('#cache-size').html(json.summary.cache_size+' kB');

            $('#requests').html(json.summary.requests);
            $('#redirects').html(json.summary.redirects);
            $('#bad-req').html(json.summary.bad_req);
            $('#hosts').html(json.summary.hosts);

            // Page Speed Score - Gauge
            that.score(json.summary.score);

            // Resources
            that.resources('by-size','Resources by Size',json.weights,' kB');
            that.resources('by-req','Resources by Count',json.requests,'');

            // Page Speed Details
            that.pagespeed(json.pagespeed);

            // HAR Viewer
            var iframe  = document.createElement('iframe');
            var url     = '/results/harviewer?inputUrl=/results/download%3Fid%3D'+json.har+'&expand=true';
            iframe.src          = url;
            iframe.width        = '940';
            iframe.height       = Math.max(Math.min(json.summary.requests*40+20,600),300).toString();
            iframe.frameBorder  = '0';

            $('#harviewer').html(iframe);
            
            // New tab feature of HAR Viewer
            var newtab = document.getElementById('newtab');
            newtab.onclick = function () {
                window.open(url);
            };

            // Hide Ajax spinner
            that.spinner.style.display = 'none';
        }
    };

    // Get timestamp from argument of function or from select box
    var selector    = document.getElementById('run_timestamp');
    var timestamp;
    if ( typeof(opt_ts) !== 'undefined' ) {
        timestamp = opt_ts;

        // Update select box
        for(var i=0, len = selector.options.length; i < len; i++) {
            if(selector.options[i].value === opt_ts) {
                selector.selectedIndex = i;
                $("#run_timestamp").trigger("liszt:updated");
                break;
            }
        }
    } else {
        timestamp   = selector.options[selector.selectedIndex].text;
    }
    var URI         = 'runinfo?timestamp=' + timestamp;

    xmlhttp.open('GET', URI, true);
    xmlhttp.send();

    // Show Ajax spinner
    this.spinner.style.display = 'block';
};

//Delete current run from set of test results
RunInfo.prototype.del = function(button,mode,all) {
    //
    var answer = window.confirm('Are you sure?');

    if (answer === true) {
        var xmlhttp = new XMLHttpRequest();

        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                var response = xmlhttp.responseText;
                window.location = response;
            }
        };

        var ts_selector = document.getElementById('run_timestamp');
        var timestamp   = ts_selector.options[ts_selector.selectedIndex].text;
        var URI = 'deleterun?timestamp=' + timestamp;
            URI += '&label=' + button.id;
            URI += '&mode=' + mode;
            URI += '&all=' + all;

        xmlhttp.open('GET', URI, true);
        xmlhttp.send();
    }
};

// Add delay for async rendering
RunInfo.prototype.changeVisibility = function () {
    var buttons = document.getElementsByTagName('button');

    for(var i = 0, len = buttons.length; i < len; i++){
        buttons[i].style.display = 'inline';
    }
};

RunInfo.prototype.timedStyleChange = function () {
    setTimeout(this.changeVisibility(), 1000);
};

RunInfo.prototype.addSpinner = function() {
    var opts = {
            lines:  10,
            length: 5,
            width:  3,
            radius: 5,
            color:  '#498a2d',
            speed:  0.8,
            trail:  80
    };
    
    this.spinner = document.getElementById('spinner');
    new Spinner(opts).spin(this.spinner);
};