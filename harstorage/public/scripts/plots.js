// draw Gauge Chart
function drawScore(score) {
    // value for chart
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Score');
    data.addColumn('number', 'Value');
    data.addRows(1);
    data.setValue(0, 0, 'PS Score');
    data.setValue(0, 1, score);

    // chart options
    var options = {
      width: 200,
      height: 200,
      redFrom: 0,
      redTo: 59,
      yellowFrom: 60,
      yellowTo: 79,
      greenFrom: 80,
      greenTo: 100,
      minorTicks: 10};

    // chart object
    var chart = new google.visualization.Gauge(document.getElementById('gauge'));
    chart.draw(data, options);
}

function drawTimeLine(timeHash,sizeHash,reqHash,scoreHash) {
    // Prepair data for charts
    var keySorted   = [];
    var timeSorted  = [];
    var sizeSorted  = [];
    var reqSorted   = [];
    var scoreSorted = [];

    for (key in timeHash) keySorted.push(key);
    keySorted.sort();

    for (var i = 0; i < keySorted.length; i++){
        timeSorted.push( timeHash[ keySorted[i] ] );
        sizeSorted.push( sizeHash[ keySorted[i] ] );
        reqSorted.push( reqHash[ keySorted[i] ] );
        scoreSorted.push( scoreHash[ keySorted[i] ] );
    }

    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'timeline_div',
            zoomType: 'x',
            alignTicks: false
        },
        exporting: {
            buttons : {
                printButton: { enabled: false}
            },
            url:'/chart/export',
            width: 960,
            filename: 'timeline'
        },
        title: { text: 'Performance Trends' },
        xAxis: [{
            categories          : keySorted,
            tickInterval        : Math.ceil(keySorted.length / 10),
            tickmarkPlacement   : 'on'
        }],
        yAxis: [{ // yAxis #1
            title: {
                text: 'Full Load Time (ms)',
                style: { color: '#DDDF0D' }
            },
            min: 0,
        }, { // yAxis #2
            title: {
                text: 'Total Requests',
                style: { color: '#55BF3B' }
            },
            min: 0,
            opposite: true
        }, { // yAxis #3
            title: {
                text: 'Total Size (kB)',
                style: { color: '#DF5353' }
            },
            min: 0,
            opposite: true
        }, { // yAxis #4
            title: {
                text: 'Page Speed Score',
                style: { color: '#7798BF' }
            },
            min: 0,
            endOnTick: false
        }],
        tooltip: {
            formatter: function() {
                    var unit = {
                        'Full Load Time': 'ms',
                        'Total Requests': '',
                        'Total Size': 'kB',
                        'Page Speed Score': ''
                    }[this.series.name];

                return '<b>' + this.y + ' ' + unit + '</b>' + ' (' + this.x + ')';
            }
        },
        series: [{
            name: 'Full Load Time',
            type: 'spline',
            yAxis: 0,
            data: timeSorted
        }, {
            name: 'Total Requests',
            type: 'spline',
            yAxis: 1,
            data: reqSorted
        }, {
            name: 'Total Size',
            type: 'spline',
            yAxis: 2,
            data: sizeSorted
        }, {
            name: 'Page Speed Score',
            type: 'spline',
            yAxis: 3,
            data: scoreSorted
        } ]
    });
}

function drawPageSpeed (json) {
    rules   = [];
    scores  = [];
    rows    = 0;

    jQuery.each(json.pagespeed, function(key,value) {
        rules.push(key);
        scores.push(value);
        rows += 1;
    });

    height = 75 + 20 * rows;

    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'pagespeed',
            defaultSeriesType: 'bar',
            height  : height,
            width   : 930, 
        },
        exporting: {
            buttons : {
                printButton: { enabled: false}
            },
            url:'/chart/export',
            width: 930,
            filename: 'pagespeed'
        },
        title: {
            text: "Page Speed Scores"
        },
        xAxis: {
            categories: rules,
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            max: 105,
            endOnTick: false,
            title: {
                text: null,
            }
        },
        tooltip: {
            formatter: function() {
                return this.x +': '+ this.y;
            }
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            },
            series: {
                showInLegend: false,
                animation: false,
            }
        },
        series: [{
            data: scores
        }]
    });
}

function drawPie(div,title,hash,units) {
    data  = [];

    jQuery.each(hash, function(key,value) {
        data.push( [key,value]);
    });

    chart = new Highcharts.Chart({
        chart: {
            renderTo: div,
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            width: 450,
            height: 300,
        },
        exporting: {
            buttons : {
                printButton: { enabled: false}
            },
            url:'/chart/export',
            width: 450,
            filename: 'resources'
        },
        title: {
            text: title,
        },
        tooltip: {
            formatter: function() {
                return '<b>'+ this.point.name +'</b>: '+ this.y + units;
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                size: '65%',
                dataLabels: {
                    enabled: true,
                    color: '#FFF',
                    distance: 25,
                    connectorColor: '#FFF',
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
}


// Ajax stuff
// Dislpay details for selected test run
function displayRunInfo() {
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            var json = eval("("+xmlhttp.responseText+")");
            
            // Page Speed Score - Gauge 
            drawScore(json.summary.score);
            
            // Summary
            $("#full-load-time").html(json.summary.full_time+' ms');
            $("#dns").html(json.summary.dns+' ms');
            $("#transfer").html(json.summary.transfer+' ms');
            $("#connecting").html(json.summary.connecting+' ms');
            $("#server").html(json.summary.server+' ms');
            $("#blocked").html(json.summary.blocked+' ms');
            
            $("#total-size").html(json.summary.total_size+' kB');
            $("#text-size").html(json.summary.text_size+' kB');
            $("#media-size").html(json.summary.media_size+' kB');
            $("#cache-size").html(json.summary.cache_size+' kB');

            $("#requests").html(json.summary.requests);
            $("#redirects").html(json.summary.redirects);
            $("#bad-req").html(json.summary.bad_req);
            $("#hosts").html(json.summary.hosts);

            // Page Speed Details
            drawPageSpeed(json);

            // Resources
            drawPie("by-size","Resources by Size",json.weights,' kB');
            drawPie("by-req","Resources by Count",json.requests,'');

            // HAR Viewer
            var iframe = document.createElement('iframe');
            iframe.src = "/results/harviewer?har="+json.har;
            iframe.width = "940";
            iframe.height = "400";
            iframe.frameBorder = "0";
            $("#harviewer").html(iframe);
        }
    }

    xmlhttp.open("POST","runinfo",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    var ts_selector = document.getElementById("run_timestamp");
    timestamp = ts_selector.options[ts_selector.selectedIndex].text;
    var parameters = "timestamp="+timestamp;

    xmlhttp.send(parameters);
}

function deleteRun(button,mode) {
    var answer = confirm ("Are you sure?");
    if (answer) {
        var xmlhttp = new XMLHttpRequest();

        xmlhttp.onreadystatechange=function()
        {
            if (xmlhttp.readyState==4 && xmlhttp.status==200) {
                var response = xmlhttp.responseText;
                window.location = response;
            }
        }

        xmlhttp.open("POST","deleterun",true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

        var ts_selector = document.getElementById("run_timestamp");
        timestamp = ts_selector.options[ts_selector.selectedIndex].text;
        var parameters = "timestamp="+timestamp+"&label="+button.id+"&mode="+mode;

        xmlhttp.send(parameters);
    }
}
