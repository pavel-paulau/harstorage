google.load('visualization', '1', {packages:['gauge']});
google.load("visualization", "1", {packages:["corechart"]});

// draw Gauge Chart,
// argument is Page Speed score
function drawScore(score) {
    // value for chart
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Score');
    data.addColumn('number', 'Value');
    data.addRows(1);
    data.setValue(0, 0, 'Page Speed');
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

// draw Line Chart,
// arguments are vAxis label and XY values
function drawTimeLine(hash,label) {
    // object size property,
    // used for hash arrays
    Object.size = function(obj) {
        var size = 0, key;
        for (key in obj) {
            if (obj.hasOwnProperty(key)) size++;
        }
        return size;
    };

    // dataset for timeline
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Timestamp');
    data.addColumn('number', label);
    data.addRows(Object.size(hash));

    var index = 0;
    for (key in hash) {
        data.setValue(index, 0, key);
        data.setValue(index, 1, hash[key]);
        index = index + 1;
    }

    // chart option: sizes, curve and axis style
    var options ={
        width           :770,
        height          :270,
        curveType       :"function",
        colors          :["#e0931a"],
        chartArea       :{left:100,top:30,width:650},
        hAxis           :{title:"Timestamp",slantedText:false,slantedTextAngle:60,maxAlternation:2},
        vAxis           :{title:label,baseline:0},
        legend          :'none',
        pointSize       :4
    }

    // chart object
    var chart = new google.visualization.LineChart(document.getElementById('timeline_div'));
    chart.draw(data, options);
}

/*
function drawSizes() {
    //var stats = result.pageStats;

    // Данные для графика
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Тип');
    data.addColumn('number', 'Размер');
    data.addRows(4);
    data.setValue(0, 0, 'CSS');
    data.setValue(0, 1, Number(stats['cssResponseBytes']));
    data.setValue(1, 0, 'HTML');
    data.setValue(1, 1, Number(stats['htmlResponseBytes']));
    data.setValue(2, 0, 'Images');
    data.setValue(2, 1, Number(stats['imageResponseBytes']));
    data.setValue(3, 0, 'JavaScript');
    data.setValue(3, 1, Number(stats['javascriptResponseBytes']));

    // Параметры графика
    var options = {
      width: 450,
      height: 250,
      is3D: true,
      legend: "bottom",
      title: "Distribution by size",
      titleTextStyle: {fontSize: 14}
    }
    
    // chart object
    var div = document.getElementById('chart_div');
    var chart = new google.visualization.PieChart(div);
    chart.draw(data, options);
}*/

// draw column chart
// argument is XY hash
function drawColumns(hash) {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Rule');
        data.addColumn('number', 'Score');

        // dataset for chart
        data.addRows(Object.size(hash));
        var index = 0;
        for (key in hash) {
            data.setValue(index, 0, key);
            data.setValue(index, 1, hash[key]);
            index = index + 1;
        }
          
        // chart options - size, colors and axis
        var options = {
            width       :900,
            height      :420,
            chartArea   :{left:100,top:10,width:750,height:150},
            colors      :['#498a2d'],
            legend      :'none',
            hAxis       :{slantedText:true,slantedTextAngle:90,maxAlternation:1},
            vAxis       :{baseline:0},
        }

        // chart object
        var chart = new google.visualization.ColumnChart(document.getElementById('page-speed'));
        chart.draw(data,options);
}


// return the value of the radio button that is checked
// return an empty string if none are checked, or
// there are no radio buttons
function getCheckedValue(radioObj) {
    if(!radioObj)
        return "";
    var radioLength = radioObj.length;
    if(radioLength == undefined)
        if(radioObj.checked)
            return radioObj.value;
        else
            return "";
    for(var i = 0; i < radioLength; i++) {
        if(radioObj[i].checked) {
            return radioObj[i].value;
        }
    }
    return "";
}

// Ajax stuff
// Dislpay details for selected test run
function displayRunInfo() {
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            var json = eval("("+xmlhttp.responseText+")")
            drawScore(json.score);

            document.getElementById("run_time").innerHTML = json.time;
            document.getElementById("run_size").innerHTML = json.size;
            document.getElementById("run_requests").innerHTML = json.requests;
            
            var pagespeed = new Array();    
            jQuery.each(json, function(key,value) {
                if (key!='time' && key!='size' && key!='requests' && key!='score'){
                    console.debug(key,value);
                    pagespeed[key]=value;
                }
            });
            drawColumns(pagespeed);
        }
     }
    xmlhttp.open("POST","runinfo",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    var ts_selector = document.getElementById("run_timestamp");
    timestamp = ts_selector.options[ts_selector.selectedIndex].text;
    var parameters = "timestamp="+timestamp
    xmlhttp.send(parameters);
}
