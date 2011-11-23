"use strict";

/*
 * Timeline chart
 */
var Timeline = function(run_info) {
    this.run_info = run_info;
};

// Get data for timeline
Timeline.prototype.get = function(url, label, mode) {
    // Pointer
    var that = this;

    // Retrieve data for timeline via XHR call
    var xhr = new XMLHttpRequest();
    
    xhr.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            that.draw(this.responseText);
        }
    };

    var URI = 'timeline?url=' + url + '&label=' + label + '&mode=' + mode;

    xhr.open('GET', URI, true);
    xhr.send();
};

// Draw timeline
Timeline.prototype.draw = function(points) {
    // Pointer
    var that = this;

    var splitResults = points.split(';');

    var tsArray     = splitResults[0].split('#'),
        timeArray   = splitResults[1].split('#'),
        sizeArray   = splitResults[2].split('#'),
        reqArray    = splitResults[3].split('#'),
        scoreArray  = splitResults[4].split('#');

    for(var index = 0, len = tsArray.length; index < len; index += 1) {
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
                            that.run_info.get(this.category);
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

    for(var index = 0, len = tsArray.length; index < len; index += 1) {
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
var RunInfo = function(mode, label) {
    // Pointer
    var that = this;

    // Initialize cache
    this.cache = {};

    // Add event handler to selector box
    var run_timestamp = document.getElementById('run_timestamp');

    run_timestamp.onchange = function() {
        that.get();
    };

    // Add event handler to delete button
    var del_btn = document.getElementById('del-btn');

    del_btn.onclick = function() {
        that.del(label, mode, false);
    };

    // Add event handler to delete all button
    var del_all_btn = document.getElementById('del-all-btn');

    del_all_btn.onclick = function() {
        that.del(label, mode, true);
    };
};

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
RunInfo.prototype.resources = function (div, title, hash, units, width) {
    // Extract data
    var data  = [];

    for(var key in hash) {
        data.push( [key, hash[key] ]);
    }

    // Chart object
    var chart = new Highcharts.Chart({
        chart: {
            renderTo            : div,
            plotBackgroundColor : null,
            plotBorderWidth     : null,
            plotShadow          : false,
            width               : width,
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
            width       : width
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

    for(var rule in pagespeed) {
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
    // Pointer
    var that = this;

    // Dynamic data
    this.json = [];

    // Show Ajax spinner
    this.spinner.style.display = 'block';

    // Update test results
    var set_data = function() {
        // Update cache
        if ( typeof(that.cache[that.URI]) === 'undefined') {
            that.json = JSON.parse(that.xhr.responseText);
            that.cache[that.URI] = that.json;
        }

        // Summary
        $('#full-load-time').html   ( that.json.summary.full_time   + ' ms' );
        $('#dns').html              ( that.json.summary.dns         + ' ms' );
        $('#transfer').html         ( that.json.summary.transfer    + ' ms' );
        $('#connecting').html       ( that.json.summary.connecting  + ' ms' );
        $('#server').html           ( that.json.summary.server      + ' ms' );
        $('#blocked').html          ( that.json.summary.blocked     + ' ms' );

        $('#total-size').html       ( that.json.summary.total_size  + ' kB' );
        $('#text-size').html        ( that.json.summary.text_size   + ' kB' );
        $('#media-size').html       ( that.json.summary.media_size  + ' kB' );
        $('#cache-size').html       ( that.json.summary.cache_size  + ' kB' );

        $('#requests').html         ( that.json.summary.requests            );
        $('#redirects').html        ( that.json.summary.redirects           );
        $('#bad-req').html          ( that.json.summary.bad_req             );
        $('#hosts').html            ( that.json.summary.hosts               );

        // Page Speed Score - Gauge
        that.score(that.json.summary.score);

        // Resources
        that.resources('by-size','Resources by Size', that.json.weights,  ' kB' , 450);
        that.resources('by-req','Resources by Requests', that.json.requests, '' , 450);

        // Domains
        that.resources('domains-by-size','Domains by Size', that.json.d_weights,     ' kB' , 930);
        that.resources('domains-by-req','Domains by Requests', that.json.d_requests, ''    , 930);

        // Page Speed Details
        that.pagespeed(that.json.pagespeed);

        // HAR Viewer
        var iframe  = document.createElement('iframe');
        var url = '/results/harviewer?inputUrl=/results/download%3Fid%3D';
            url += that.json.har;
            url += '&expand=true';

        var height = Math.max(Math.min(that.json.summary.requests*40+20, 600), 300).toString();

        iframe.src          = url;
        iframe.width        = '940';
        iframe.height       = height;
        iframe.frameBorder  = '0';

        $('#harviewer').html(iframe);

        // New tab feature of HAR Viewer
        var newtab = document.getElementById('newtab');
        newtab.onclick = function () {
            window.open(url);
        };

        // Hide Ajax spinner
        that.spinner.style.display = 'none';
    };

    // Request data via XHR or read from cache
    
    // Get timestamp from argument of function or from select box
    var selector    = document.getElementById('run_timestamp');
    var timestamp;

    if ( typeof(opt_ts) !== 'undefined' ) {
        timestamp = opt_ts;

        // Update select box
        for(var i = 0, len = selector.options.length; i < len; i += 1 ) {
            if(selector.options[i].value === opt_ts) {
                selector.selectedIndex = i;
                $('#run_timestamp').trigger('liszt:updated');
            }
        }
    } else {
        timestamp   = selector.options[selector.selectedIndex].text;
    }

    this.URI = 'runinfo?timestamp=' + timestamp;

    this.xhr = new XMLHttpRequest();

    this.xhr.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            set_data();
        }
    };

    if ( typeof(this.cache[this.URI]) === 'undefined' ) {
        this.xhr.open('GET', this.URI, true);
        this.xhr.send();
    } else {
        this.json = this.cache[this.URI];
        set_data();
    }
};

//Delete current run from set of test results
RunInfo.prototype.del = function(id, mode, all) {
    //
    var answer = window.confirm('Are you sure?');

    if (answer === true) {
        var xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function() {
            if (this.readyState === 4 && this.status === 200) {
                window.location = this.responseText;
            }
        };

        var ts_selector = document.getElementById('run_timestamp');
        var timestamp   = ts_selector.options[ts_selector.selectedIndex].text;
        var URI = 'deleterun?timestamp=' + timestamp;
            URI += '&label=' + id;
            URI += '&mode=' + mode;
            URI += '&all=' + all;

        xhr.open('GET', URI, true);
        xhr.send();
    }
};

// Add delay for async rendering
RunInfo.prototype.changeVisibility = function () {
    var del_btn     = document.getElementById('del-btn'),
        del_all_btn = document.getElementById('del-all-btn'),
        newtab_btn  = document.getElementById('newtab');    
    
    del_btn.style.display       = 'inline';
    del_all_btn.style.display   = 'inline';
    newtab_btn.style.display    = 'inline';
};

RunInfo.prototype.timedStyleChange = function () {
    setTimeout(this.changeVisibility, 1000);    
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