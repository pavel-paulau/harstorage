"use strict";

/*
 * Name space
 */
var HARSTORAGE = HARSTORAGE || {};

/*
 * Timeline chart
 */
HARSTORAGE.Timeline = function(run_info) {
    this.run_info = run_info;
};

// Get data for timeline
HARSTORAGE.Timeline.prototype.get = function(url, label, mode) {
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
HARSTORAGE.Timeline.prototype.draw = function(points) {
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
    
    // Colors for Y Axis labels
    var theme = HARSTORAGE.read_cookie('chartTheme');

    var colors = [];

    if (theme === 'dark-green' || !theme) {
        colors = [
            '#DDDF0D',
            '#55BF3B',
            '#DF5353',
            '#7798BF',
            '#6AF9C4',
            '#DB843D',
            '#EEAAEE'
        ];
    } else {
        colors = [
            '#669933',
            '#CC3333',
            '#FF9933',
            '#996633',
            '#4572A7',
            '#80699B',
            '#92A8CD',
            '#A47D7C'
        ];
    }
    
    new Highcharts.Chart({
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
                style   : {
                    color   : colors[0]
                }
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
                style   : {
                    color   : colors[1]
                }
            },
            min         : 0,
            opposite    : true
        }, { // yAxis #3
            title: {
                text    : 'Total Size (kB)',
                style   : {
                    color   : colors[2]
                }
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
                style   : {
                    color   : colors[3]
                }
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
HARSTORAGE.Columns = function() {};

HARSTORAGE.Columns.prototype.draw = function(points) {
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

    // Colors for Y Axis labels
    var theme = HARSTORAGE.read_cookie('chartTheme');

    var colors = [];

    if (theme === 'dark-green' || !theme) {
        colors = [
            '#DDDF0D',
            '#55BF3B',
            '#DF5353',
            '#7798BF',
            '#6AF9C4',
            '#DB843D',
            '#EEAAEE'
        ];
    } else {
        colors = [
            '#669933',
            '#CC3333',
            '#FF9933',
            '#996633',
            '#4572A7',
            '#80699B',
            '#92A8CD',
            '#A47D7C'
        ];
    }

    new Highcharts.Chart({
        chart: {
            renderTo    : 'chart'
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
                style   : {
                    color   : colors[0]
                }
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
                style   : {
                    color   : colors[1]
                }
            },
            min         : 0,
            opposite    : true
        }, { // yAxis #3
            title: {
                text    : 'Total Size (kB)',
                style   : {
                    color   : colors[2]
                }
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
                style   : {
                    color   : colors[3]
                }
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
                events: {
                    hide: function() {
                        this.yAxis.axisTitle.hide();
                    },
                    show: function() {
                        this.yAxis.axisTitle.show();
                    }
                }
            }
        },
        series: [{
            name    : 'Full Load Time',
            type    : 'column',
            yAxis   : 0,
            data    : timeArray
        }, {
            name    : 'Total Requests',
            type    : 'column',
            yAxis   : 1,
            data    : reqArray
        }, {
            name    : 'Total Size',
            type    : 'column',
            yAxis   : 2,
            data    : sizeArray
        }, {
            name    : 'Page Speed Score',
            type    : 'column',
            yAxis   : 3,
            data    : scoreArray
        }]
    });
};

/*
 * Test results
 */
HARSTORAGE.RunInfo = function(mode, label, query) {
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

    // Add event handler to aggregation button
    var agg_btn = document.getElementById('agg-btn');

    if (query !== 'None') {
        agg_btn.style.display = 'inline';
        agg_btn.onclick = function() {
            location.href = query.replace(/amp;/g,'');
        };
    }
};

//Page Resources
HARSTORAGE.RunInfo.prototype.resources = function (div, title, hash, units, width) {
    // Extract data
    var data  = [];

    for(var key in hash) {
        if (hash.hasOwnProperty(key)) {
            data.push( [key, hash[key] ]);
        }
    }

    // Chart object
    new Highcharts.Chart({
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
HARSTORAGE.RunInfo.prototype.pagespeed = function (pagespeed) {
    // Spliting data for chart
    var rules   = ['Total Score'],
        scores  = [pagespeed['Total Score']];

    for(var rule in pagespeed) {
        if (pagespeed.hasOwnProperty(rule) && rule !== 'Total Score' ) {
            rules.push(rule);
            scores.push(pagespeed[rule]);
        }
    }

    // Chart height
    var height = Math.max(75 + 20 * rules.length, 100);

    // Chart object
    new Highcharts.Chart({
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
            categories  : rules,
            labels: {
                formatter: function() {
                    if (this.value === 'Total Score') {
                        return '<b>@' + this.value + '</b>';
                    } else {
                        return this.value;
                    }
                }
            }
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
HARSTORAGE.RunInfo.prototype.get = function(opt_ts) {
    // Pointer
    var that = this;

    // Dynamic data
    this.json = [];

    // Show Ajax spinner
    this.spinner.style.display = 'block';

    // Formatter
    this.formatter = function(value, units) {
        // Default units
        if ( typeof(units) === 'undefined') {
            units = '';
        }

        // Formatter
        switch ( typeof(value) ) {
        case "number":
            if (value >= 1000) {
                var seconds = Math.floor(value/1000);
                var milliseconds = value - seconds*1000;

                if (milliseconds < 10) {
                    milliseconds = "00" + milliseconds;
                } else if (milliseconds < 100) {
                    milliseconds = "0" + milliseconds;
                }
                
                return seconds + ' ' +  milliseconds + ' ' + units;
            } else {
                return value + ' ' + units;
            }
        case "string":
            return value;            
        default:
            return "n/a";
        }
    };

    // Update test results
    var set_data = function() {
        // Update cache
        if ( typeof(that.cache[that.URI]) === 'undefined') {
            that.json = JSON.parse(that.xhr.responseText);
            that.cache[that.URI] = that.json;
        }

        // Summary
        $('#full-load-time').html       ( that.formatter(that.json.summary.full_load_time,      'ms') );
        $('#onload-event').html         ( that.formatter(that.json.summary.onload_event,        'ms') );
        $('#start-render-time').html    ( that.formatter(that.json.summary.start_render_time,   'ms') );
        $('#time-to-first-byte').html   ( that.formatter(that.json.summary.time_to_first_byte,  'ms') );

        $('#total-dns-time').html       ( that.formatter(that.json.summary.total_dns_time,      'ms') );
        $('#total-transfer-time').html  ( that.formatter(that.json.summary.total_transfer_time, 'ms') );
        $('#total-server-time').html    ( that.formatter(that.json.summary.total_server_time,   'ms') );
        $('#avg-connecting-time').html  ( that.formatter(that.json.summary.avg_connecting_time, 'ms') );
        $('#avg-blocking-time').html    ( that.formatter(that.json.summary.avg_blocking_time,   'ms') );

        $('#total-size').html           ( that.formatter(that.json.summary.total_size,          'kB') );
        $('#text-size').html            ( that.formatter(that.json.summary.text_size,           'kB') );
        $('#media-size').html           ( that.formatter(that.json.summary.media_size,          'kB') );
        $('#cache-size').html           ( that.formatter(that.json.summary.cache_size,          'kB') );

        $('#requests').html             ( that.formatter(that.json.summary.requests                 ) );
        $('#redirects').html            ( that.formatter(that.json.summary.redirects                ) );
        $('#bad-requests').html         ( that.formatter(that.json.summary.bad_requests             ) );
        $('#domains').html              ( that.formatter(that.json.summary.domains                  ) );

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

        iframe.setAttribute('src', url);
        iframe.setAttribute('width', '940');
        iframe.setAttribute('id', 'harviewer-iframe');
        iframe.setAttribute('frameBorder', '0');
        iframe.setAttribute('frameBorder', '0');
        iframe.setAttribute('scrolling', 'no');

        $('#harviewer').html(iframe);

        window.setInterval("HARSTORAGE.autoHeight()", 100);

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
HARSTORAGE.RunInfo.prototype.del = function(id, mode, all) {
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
HARSTORAGE.RunInfo.prototype.changeVisibility = function () {
    var del_btn     = document.getElementById('del-btn'),
        del_all_btn = document.getElementById('del-all-btn'),
        newtab_btn  = document.getElementById('newtab');
    
    del_btn.style.display       = 'inline';
    del_all_btn.style.display   = 'inline';
    newtab_btn.style.display    = 'inline';
};

HARSTORAGE.RunInfo.prototype.timedStyleChange = function () {
    setTimeout(this.changeVisibility, 1000);    
};

HARSTORAGE.RunInfo.prototype.addSpinner = function() {
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

/*
 * Auto Height module
 */
HARSTORAGE.autoHeight = function() {
    var iframe = document.getElementById('harviewer-iframe');
    iframe.height = iframe.contentDocument.body.offsetHeight;
};

/*
 * Aggregated Statistics
 */
HARSTORAGE.AggregatedStatistics = function() {
    // Determine metric type from Query string
    var metric,
        href;

    if (location.href.indexOf('metric') === -1) {
        href = location.href + '&metric=';
        metric = 'Average';
    } else {
        href = location.href.split('metric')[0] + 'metric=';
        metric = location.href.split('metric')[1].split('=')[1];

        if (metric === '90th%20Percentile') {
            metric = '90th Percentile';
        }
    }

    // Update selector box active option
    var selector = document.getElementById('metrics');

    for(var i = 0, len = selector.options.length; i < len; i += 1 ) {
        if(selector.options[i].value === metric) {
            selector.selectedIndex = i;
            $('#metrics').trigger('liszt:updated');
            break;
        }
    }

    // Add event handler to selector box
    selector.onchange = function() {
        location.href = href + this.value;
    };
};