google.load('visualization', '1', {packages:['gauge']});

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
            }
        },
        title: { text: 'Performance Trends' },
        xAxis: [{
            categories      : keySorted,
            tickInterval    : Math.ceil(keySorted.length / 15)
        }],
        yAxis: [{ // yAxis #1
            title: {
                text: 'Full Time (ms)',
                style: { color: '#DDDF0D' }
            },
        }, { // yAxis #2
            title: {
                text: 'Total Requests',
                style: { color: '#55BF3B' }
            },
            opposite: true
        }, { // yAxis #3
            title: {
                text: 'Total Size',
                style: { color: '#DF5353' }
            },
            opposite: true
        }, { // yAxis #4
            title: {
                text: 'Page Speed Score',
                style: { color: '#7798BF' }
            },
            min: 0.0,
            max: 100,
        }],
        tooltip: {
            formatter: function() {
                return this.y + ' (' + this.x + ')';
            }
        },
        series: [{
            name: 'Full Time',
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

    jQuery.each(json.pagespeed, function(key,value) {
        rules.push(key);
        scores.push(value);
    });

    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'pagespeed',
            defaultSeriesType: 'bar',
            height  : 550,
            width   : 930, 
        },
        exporting: {
            buttons : {
                printButton: { enabled: false}
            }
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
            }
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

            drawScore(json.summary.score);
            
            $("#run-time").html(json.summary.time)
            $("#run-size").html(json.summary.size)
            $("#run-requests").html(json.summary.requests)

            drawPageSpeed(json);

            drawPie("by-size","Resources by Size",json.weights,' kB');
            drawPie("by-req","Resources by Count",json.requests,'');

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
