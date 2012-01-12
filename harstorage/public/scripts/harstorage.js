/*
 * Name space
 */
var HARSTORAGE = HARSTORAGE || {};

/*
 * Timeline chart
 */
HARSTORAGE.Timeline = function(run_info) {
    "use strict";

    this.run_info = run_info;
};

// Get data for timeline
HARSTORAGE.Timeline.prototype.get = function(url, label, mode) {
    "use strict";

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
    "use strict";

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
            '#FF9944',
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
        }]
    });
};

/*
 * Column Chart
 */
HARSTORAGE.Columns = function() {
    "use strict";
};

HARSTORAGE.Columns.prototype.draw = function(points, chart_type) {
    "use strict";

    // Chart type
    chart_type = (typeof(chart_type) !== 'undefined') ? chart_type : 'column';

    // Chart points
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
            '#FF9944',
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
            type    : chart_type,
            yAxis   : 0,
            data    : timeArray
        }, {
            name    : 'Total Requests',
            type    : chart_type,
            yAxis   : 1,
            data    : reqArray
        }, {
            name    : 'Total Size',
            type    : chart_type,
            yAxis   : 2,
            data    : sizeArray
        }, {
            name    : 'Page Speed Score',
            type    : chart_type,
            yAxis   : 3,
            data    : scoreArray
        }]
    });
};

/*
 * Test results
 */
HARSTORAGE.RunInfo = function(mode, label, query) {
    "use strict";

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
            location.href = query.replace(/amp;/g,'') + '&chart=column&table=true';
        };
    }
};

//Page Resources
HARSTORAGE.RunInfo.prototype.resources = function (div, title, hash, units, width) {
    "use strict";

    // Extract data
    var data  = [];

    for(var key in hash) {
        if (hash.hasOwnProperty(key)) {
            data.push( [key, hash[key] ]);
        }
    }

    // Chart object
    return new Highcharts.Chart({
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
    "use strict";

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
    return new Highcharts.Chart({
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
            categories : rules,
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
    "use strict";

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

        // Resources by Size
        setTimeout(
            function() {
                that.resources('by-size', 'Resources by Size', that.json.weights, ' kB', 450);
            },
            50
        );

        // Resources by Requests
        setTimeout(
            function() {
                that.resources('by-req', 'Resources by Requests', that.json.requests, '', 450);
            },
            150
        );

        // Domains by Size
        setTimeout(
            function() {
                that.resources('domains-by-size', 'Domains by Size', that.json.d_weights, ' kB', 930);
            },
            250
        );

        // Domains by Requests
        setTimeout(
            function() {
                that.resources('domains-by-req', 'Domains by Requests', that.json.d_requests, '', 930);
            },
            350
        );

        // Page Speed Details
        setTimeout(
            function() {
                that.pagespeed(that.json.pagespeed);
            },
            450
        );

        // Hide Ajax spinner
        that.spinner.style.display = 'none';
    };

    // Request data via XHR or read from cache
    
    // Get timestamp from argument of function or from select box
    var selector = document.getElementById('run_timestamp'),
        timestamp;

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
    "use strict";

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
    "use strict";

    var del_btn     = document.getElementById('del-btn'),
        del_all_btn = document.getElementById('del-all-btn'),
        newtab_btn  = document.getElementById('newtab');
    
    del_btn.style.display       = 'inline';
    del_all_btn.style.display   = 'inline';
    newtab_btn.style.display    = 'inline';
};

HARSTORAGE.RunInfo.prototype.timedStyleChange = function () {
    "use strict";

    setTimeout(this.changeVisibility, 1000);
};

HARSTORAGE.RunInfo.prototype.addSpinner = function() {
    "use strict";

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
    "use strict";

    var iframe = document.getElementById('harviewer-iframe');
    iframe.height = iframe.contentDocument.body.offsetHeight;
};

/*
 * Aggregated Statistics
 */
HARSTORAGE.AggregatedStatistics = function() {
    "use strict";

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

/*
 * Superpose Form
 */
HARSTORAGE.SuperposeForm = function() {
    "use strict";

    var that = this;

    // Initialize cache
    this.cache = {};

    // Select box event handler
    var selector = document.getElementById('step_1_label');
    selector.onchange = function() {
        that.setTimestamps(this.name);
    };

    // Submit button event handler
    var submit = document.getElementById('submit');
    submit.onclick = function() {
        return that.submit();
    };

    // Add button event handler
    var add = document.getElementById('step_1_add');
    add.onclick = function() {
        that.add(this);
    };

    // Delete button event handler
    var del = document.getElementById('step_1_del');
    del.onclick = function() {
        that.del(this);
    };
    del.style.display = 'none';

    // Chart options
    var checkbox = document.getElementById('column');
    checkbox.onclick = function() {
        that.checkbox(this);
    };

    checkbox = document.getElementById('spline');
    checkbox.onclick = function() {
        that.checkbox(this);
    };
};

// Form validation
HARSTORAGE.SuperposeForm.prototype.submit = function() {
    "use strict";

    var selectors = document.getElementsByTagName('select');

    for(var i = 0, len = selectors.length/3; i < len; i += 1) {
        var id = 1 + i*3;

        var start_ts    = selectors.item(id).options[ selectors.item(id).options.selectedIndex ].value;
        var end_ts      = selectors.item(id+1).options[ selectors.item(id+1).options.selectedIndex ].value;

        if (end_ts < start_ts) {
            window.alert('Invalid timestamps!');
            return false;
        }
    }

    var form = document.getElementById('superpose-form');
    form.onsubmit = 'return true;';

    return true;
};

// Add new step
HARSTORAGE.SuperposeForm.prototype.add = function(button) {
    "use strict";

    var i,
        len,
        prev_button;

    var that = this;

    // Find previous and new id
    var prev_id = button.id.split('_')[0] + '_' + button.id.split('_')[1];
    var new_id = prev_id.split('_')[0] + '_' + ( parseInt ( prev_id.split('_')[1], 10) +1 );

    // Add new line to container
    var prev_div = document.getElementById(prev_id);
    var new_div = prev_div.cloneNode(true);

    new_div.setAttribute('id', new_id);

    var container = document.getElementById('container');
    container.appendChild(new_div);

    // Update name and id of selectors
    var selectors = new_div.getElementsByTagName('select');

    for(i = selectors.length; i -- ; ) {
        switch (selectors.item(i).name) {
        case prev_id + '_label':
            selectors.item(i).name  = new_id + '_label';
            selectors.item(i).id    = new_id + '_label';
            selectors.item(i).onchange = function() {
                that.setTimestamps(this.name);
            };
            break;
        case prev_id + '_start_ts':
            selectors.item(i).name  = new_id + '_start_ts';
            selectors.item(i).id    = new_id + '_start_ts';
            break;
        case prev_id + '_end_ts':
            selectors.item(i).name  = new_id + '_end_ts';
            selectors.item(i).id    = new_id + '_end_ts';
            break;
        default:
            break;
        }
    }

    // Update inputs
    var inputs = new_div.getElementsByTagName('input');

    for(i = 0, len = inputs.length; i < len; i += 1) {
        switch (inputs.item(i).id) {
        case prev_id + '_add':
            // Set new id
            inputs.item(i).id = new_id + '_add';

            // Hide previous button
            prev_button = document.getElementById(prev_id + '_add');
            prev_button.style.display = 'none';

            // Set event handler
            inputs.item(i).onclick = function() {
                that.add(this);
            };
            break;
        case prev_id + '_del':
            // Set new id
            inputs.item(i).id = new_id + '_del';

            // Hide previous button
            prev_button = document.getElementById(prev_id + '_del');
            prev_button.style.display = 'none';

            // Show current button
            inputs.item(i).style.display = 'inline';

            // Set event handler
            inputs.item(i).onclick = function() {
                that.del(this);
            };
            break;
        default:
            break;
        }
    }
    // Update head
    var divs = new_div.getElementsByTagName('div');

    for(i = 0, len = divs.length; i < len; i += 1) {
        if (divs.item(i).id === prev_id + '_head' ) {
            // New id
            divs.item(i).id = new_id + '_head';

            // New label
            divs.item(i).innerHTML = 'Set ' + new_id.split('_')[1] + ' &gt;';
        }
    }

    // Update timestamp
    this.setTimestamps(new_id + '_label');
};

// Delete selected step
HARSTORAGE.SuperposeForm.prototype.del = function(button) {
    "use strict";

    var prev_button;

    // Calculate id
    var id      = button.id.split('_')[0] + '_' + button.id.split('_')[1];
    var prev_id = button.id.split('_')[0] + '_' + ( parseInt ( button.id.split('_')[1], 10) - 1 );

    // Get DIVs
    var div         = document.getElementById(id);
    var container   = document.getElementById('container');

    // Delete current line
    container.removeChild(div);

    // Show previous button
    prev_button = document.getElementById(prev_id + '_add');
    prev_button.style.display = 'inline';

    if (prev_id !== 'step_1') {
        prev_button = document.getElementById(prev_id + '_del');
        prev_button.style.display = 'inline';
    }
};

// Set timelines for selected label
HARSTORAGE.SuperposeForm.prototype.setTimestamps = function(id) {
    "use strict";

    // Poiner
    var that = this;

    // Dynamic data
    this.dates = [];

    // Show Ajax spinner
    this.spinner.style.display = 'block';

    // Update timestamps
    var set_data = function() {
        var i,
            len,
            ts;

        // Calculate id
        id  = id.split('_')[0] + '_' + id.split('_')[1];

        // Hide Ajax spinner
        that.spinner.style.display = 'none';

        // Update cache
        if ( typeof(that.cache[that.URI]) === 'undefined') {
            that.dates = that.xhr.responseText.split(';');
            that.cache[that.URI] = that.dates;
        } else {
            that.dates.reverse();
        }

        // Start timestamps
        var select = document.getElementById(id + '_start_ts');
        select.options.length = 0;

        for(i = 0, len = that.dates.length; i < len; i += 1) {
            ts = that.dates[i];
            select.options[i] = new Option(ts, ts, false, false);
        }

        // End timestamps
        select = document.getElementById(id + '_end_ts');
        select.options.length = 0;
        that.dates.reverse();

        for(i = 0, len = that.dates.length; i < len; i += 1) {
            ts = that.dates[i];
            select.options[i] = new Option(ts, ts, false, false);
        }
    };

    // Request data via XHR or read from cache
    var select = document.getElementById(id);
    var label = select.options[select.selectedIndex].text;
    this.URI = 'dates?label=' + label;

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
        this.dates = this.cache[this.URI];
        set_data();
    }
};
// Add Ajax spinner
HARSTORAGE.SuperposeForm.prototype.addSpinner = function() {
    "use strict";

    var opts = {
            lines: 10,
            length: 6,
            width: 3,
            radius: 6,
            color: '#498a2d',
            speed: 0.8,
            trail: 80
        };

    this.spinner = document.getElementById('spinner');
    new Spinner(opts).spin(this.spinner);
};

// Checkbox group
HARSTORAGE.SuperposeForm.prototype.checkbox = function(input) {
    "use strict";

    var id1  = 'spline',
        id2  = 'column',
        id;

    if (input.checked) {
        id = (input.id === id1) ? id2 : id1;
        var checkbox = document.getElementById(id);
        checkbox.checked = false;
    }
};