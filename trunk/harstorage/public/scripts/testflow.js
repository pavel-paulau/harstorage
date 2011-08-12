function submitFlow(){
    document.forms["testFlowForm"].onsubmit="return true;"
}

function addStep(button){
    // Find previous and new id
    prev_id = button.id.split("_")[0] + "_" + button.id.split("_")[1];
    new_id = prev_id.split("_")[0] + '_' + ( parseInt ( prev_id.split("_")[1], 10) +1 );
    
    // Add new line to DIV container
    prev_div = document.getElementById(prev_id);
    var new_div = prev_div.cloneNode(true);
    new_div.setAttribute('id',new_id );

    var container = document.getElementById('container');
    container.appendChild(new_div);

    // Update name and id of selectors
    selectors = new_div.getElementsByTagName('select');
    for(var i = 0; i < selectors.length; i++)
    {
        if(selectors.item(i).name == prev_id + '_label' )
        {
            selectors.item(i).name = new_id + '_label';
            selectors.item(i).id = new_id + '_label';
        }
        if(selectors.item(i).name == prev_id + '_start_ts' )
        {
            selectors.item(i).name = new_id + '_start_ts';
            selectors.item(i).id = new_id + '_start_ts';
        }
        if(selectors.item(i).name == prev_id + '_end_ts' )
        {
            selectors.item(i).name = new_id + '_end_ts';
            selectors.item(i).id = new_id + '_end_ts';
        }
    }

    // Update inputs
    inputs = new_div.getElementsByTagName('input');
    for(var i = 0; i < inputs.length; i++)
    {
        if(inputs.item(i).id == prev_id + '_add')
        {
            // Set new id
            inputs.item(i).id = new_id + '_add';
            // Hide previous button
            var prev_button = document.getElementById(prev_id + '_add');
            prev_button.style.display = "none";
        }
        if(inputs.item(i).id == prev_id + '_del')
        {
            // Set new id
            inputs.item(i).id = new_id + '_del';
            // Hide previous button
            var prev_button = document.getElementById(prev_id + '_del');
            prev_button.style.display = "none";
            // Show current button
            inputs.item(i).style.display = "inline";
        }

    }
    // Update head
    divs = new_div.getElementsByTagName('div');
    for(var i = 0; i < divs.length; i++)
    {
        if(divs.item(i).id == prev_id + '_head' )
        {
            // New id
            divs.item(i).id = new_id + '_head';
            // New label
            divs.item(i).innerHTML = 'Step ' + new_id.split('_')[1] + ' &gt;';
        }
    }
    // Update timestamp
    setTimestamp(new_id + "_label");
}

function delStep(button){
    // Calculate id
    id      = button.id.split('_')[0] + '_' + button.id.split('_')[1];
    prev_id = button.id.split("_")[0] + '_' + ( parseInt ( button.id.split("_")[1], 10) - 1 );

    // Get DIVs
    var div         = document.getElementById(id);
    var container   = document.getElementById("container");

    // Delete current line
    container.removeChild(div);

    // Show previous button
    var prev_button = document.getElementById(prev_id + '_add');
    prev_button.style.display = "inline";

    if (prev_id != 'step_1') {
        var prev_button = document.getElementById(prev_id + '_del');
        prev_button.style.display = "inline";
    }
}

function sortNumber(a,b)
{
    return b - a;
}

function setTimestamp(id){
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            // Calculate Id
            id  = id.split('_')[0] + '_' + id.split('_')[1];
            // Timestamps for response
            var timestamps = eval("("+xmlhttp.responseText+")");

            // Sorted timestamps
            var keySorted   = [];
            for (key in timestamps) keySorted.push(parseInt(key));
            keySorted.sort(sortNumber);

            // Start TS
            select = document.getElementById(id + '_start_ts');
            select.options.length = 0;

            for (var i = 0; i < keySorted.length; i++){
                ts = timestamps[ keySorted[i] ];
                select.options[i]=new Option(ts, ts, false, false);
            }

            // End TS
            select = document.getElementById(id + '_end_ts');
            select.options.length = 0;
            keySorted.reverse();

            for (var i = 0; i < keySorted.length; i++){
                ts = timestamps[ keySorted[i] ];
                
                select.options[i]=new Option(ts, ts, false, false);
            }
        }
    }

    xmlhttp.open("POST","dates",true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    select = document.getElementById(id);
    label = select.options[select.selectedIndex].text;

    var parameters = "label="+label;

    xmlhttp.send(parameters);
}
