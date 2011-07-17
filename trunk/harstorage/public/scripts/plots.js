google.load('visualization', '1', {packages:['gauge']});
google.load("visualization", "1", {packages:["corechart"]});

// object size property,
// used for hash arrays
Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};


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


// draw pie chart
function drawSizes(div_id,title,hash) {
    // dataset for chart
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Type');
    data.addColumn('number', 'Vaoue');

    data.addRows(Object.size(hash));
    var index = 0;
    for (key in hash) {
        data.setValue(index, 0, key);
        data.setValue(index, 1, hash[key]);
        index = index + 1;
    }
    
    // chart options
    var options = {
        width       :240,
        height      :210,
        chartArea   :{left:0,top:20,width:"100%"},
        is3D        :false,
        title       :title,
        legend      :"bottom",
    }
    
    // chart object
    var div = document.getElementById(div_id);
    var chart = new google.visualization.PieChart(div);
    chart.draw(data, options);
}

// draw column chart
// argument is XY hash
function drawColumns(hash) {
    // dataset for chart

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Rule');
    data.addColumn('number', 'Score');

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
    var chart = new google.visualization.ColumnChart(document.getElementById('pagespeed'));
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
            var json = eval("("+xmlhttp.responseText+")");

            drawScore(json.summary.score);

            document.getElementById("run_time").innerHTML = json.summary.time;
            document.getElementById("run_size").innerHTML = json.summary.size;
            document.getElementById("run_requests").innerHTML = json.summary.requests;

            var pagespeed = new Array();    
            jQuery.each(json.pagespeed, function(key,value) {
                pagespeed[key]=value;
            });
            drawColumns(pagespeed);

            drawSizes("by_size","Resources by Size",json.weights);
            drawSizes("by_req","Resources by Requests",json.requests);

            //console.debug(json.har);
            document.getElementById("harframe").src = "/results/harviewer?har="+json.har;
        }
    }
    xmlhttp.open("POST","runinfo",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    var ts_selector = document.getElementById("run_timestamp");
    timestamp = ts_selector.options[ts_selector.selectedIndex].text;
    var parameters = "timestamp="+timestamp;

    xmlhttp.send(parameters);
}
