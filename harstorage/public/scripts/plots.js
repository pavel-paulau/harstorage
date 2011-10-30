"use strict";

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

function setTimeLine(url,label,mode){
    // Retrieve data for timeline via XHR calls
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange=function()
    {
            if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                    drawTimeLine(xmlhttp.responseText);
            }
    };

    var URI = "timeline?url=" + url + "&label=" + label + "&mode=" + mode;

    xmlhttp.open("GET",URI,true);
    xmlhttp.send();
}

function drawTimeLine(points) {
    var index;

    var splitResults = points.split(';');

    var tsArray     = splitResults[0].split('#');
    var timeArray   = splitResults[1].split('#');
    var sizeArray   = splitResults[2].split('#');
    var reqArray    = splitResults[3].split('#');
    var scoreArray  = splitResults[4].split('#');

    for (index = 0; index < tsArray.length; index++) {
        timeArray[index]    =   parseInt(timeArray[index]);
        sizeArray[index]    =   parseInt(sizeArray[index]);
        reqArray[index]     =   parseInt(reqArray[index]);
        scoreArray[index]   =   parseInt(scoreArray[index]);
    }

    var chart = new Highcharts.Chart({
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
            categories          : tsArray,
            tickInterval        : Math.ceil(tsArray.length / 10),
            tickmarkPlacement   : 'on'
        }],
        yAxis: [{ // yAxis #1
            title: {
                text: 'Full Load Time (ms)',
                style: { color: '#DDDF0D' }
            },
            min: 0
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
            data: timeArray
        }, {
            name: 'Total Requests',
            type: 'spline',
            yAxis: 1,
            data: reqArray
        }, {
            name: 'Total Size',
            type: 'spline',
            yAxis: 2,
            data: sizeArray
        }, {
            name: 'Page Speed Score',
            type: 'spline',
            yAxis: 3,
            data: scoreArray
        } ]
    });
}

function drawPageSpeed (json) {
    var rules   = [];
    var scores  = [];
    var rows    = 0;

    jQuery.each(json.pagespeed, function(key,value) {
        rules.push(key);
        scores.push(value);
        rows += 1;
    });

    var height = 75 + 20 * rows;

    var chart = new Highcharts.Chart({
        chart: {
            renderTo: 'pagespeed',
            defaultSeriesType: 'bar',
            height  : height,
            width   : 930
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
                text: null
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
                animation: false
            }
        },
        series: [{
            data: scores
        }]
    });
}

function drawPie(div,title,hash,units) {
    var data  = [];

    jQuery.each(hash, function(key,value) {
        data.push( [key,value]);
    });

    var chart = new Highcharts.Chart({
        chart: {
            renderTo: div,
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            width: 450,
            height: 300
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
            text: title
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

    xmlhttp.onreadystatechange = function()
    {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            var json = eval("("+xmlhttp.responseText+")");
            
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

            // Page Speed Score - Gauge
            drawScore(json.summary.score);

            // Resources
            drawPie("by-size","Resources by Size",json.weights,' kB');
            drawPie("by-req","Resources by Count",json.requests,'');

            // Page Speed Details
            drawPageSpeed(json);

            // HAR Viewer
            var iframe = document.createElement('iframe');
            iframe.src = "/results/harviewer?inputUrl=/results/download%3Fid%3D"+json.har+"&expand=true";
            iframe.width = "940";
            iframe.height = "600";
            iframe.frameBorder = "0";
            $("#harviewer").html(iframe);
        }
    };

    var ts_selector = document.getElementById("run_timestamp");
    var timestamp   = ts_selector.options[ts_selector.selectedIndex].text;
    var URI  = "runinfo?timestamp=" + timestamp;

    xmlhttp.open("GET",URI,true);
    xmlhttp.send();
}

function deleteRun(button,mode) {
    var answer = confirm ("Are you sure?");
    if (answer) {
        var xmlhttp = new XMLHttpRequest();

        xmlhttp.onreadystatechange = function()
        {
            if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                var response = xmlhttp.responseText;
                window.location = response;
            }
        };

        var ts_selector = document.getElementById("run_timestamp");
        var timestamp   = ts_selector.options[ts_selector.selectedIndex].text;
        var URI = "deleterun?timestamp=" + timestamp + "&label="+ button.id + "&mode=" + mode;

        xmlhttp.open("GET",URI,true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.send();
    }
}