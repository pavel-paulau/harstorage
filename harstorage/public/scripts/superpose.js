"use strict";

// Common function
function sortNumber(a, b) {
    return b - a;
}

var SuperposeForm = function() {};

// Form validation
SuperposeForm.prototype.submit = function() {
    var selectors = document.getElementsByTagName('select');
    
    for(var i = 0, len = selectors.length/3; i < len; i++){
        var id = 1 + i*3;

        var start_ts    = selectors.item(id).options[ selectors.item(id).options.selectedIndex ].value;
        var end_ts      = selectors.item(id+1).options[ selectors.item(id+1).options.selectedIndex ].value;

        if (end_ts < start_ts) {
            window.alert('Invalid timestamps!');
            return false;
        }
    }
    document.forms.SuperposeForm.onsubmit='return true';

    return true;
};

// Add new step
SuperposeForm.prototype.add = function(button) {
    var i,
        len,
        prev_button;
        
    // Find previous and new id
    var prev_id = button.id.split('_')[0] + '_' + button.id.split('_')[1];
    var new_id = prev_id.split('_')[0] + '_' + ( parseInt ( prev_id.split('_')[1], 10) +1 );
    
    // Add new line to container
    var prev_div = document.getElementById(prev_id);
    var new_div = prev_div.cloneNode(true);

    new_div.setAttribute('id',new_id );

    var container = document.getElementById('container');
    container.appendChild(new_div);

    // Update name and id of selectors
    var selectors = new_div.getElementsByTagName('select');
    for(i = 0, len = selectors.length; i < len; i++)
    {
        if(selectors.item(i).name === prev_id + '_label' )
        {
            selectors.item(i).name  = new_id + '_label';
            selectors.item(i).id    = new_id + '_label';
        }
        if(selectors.item(i).name === prev_id + '_start_ts' )
        {
            selectors.item(i).name  = new_id + '_start_ts';
            selectors.item(i).id    = new_id + '_start_ts';
        }
        if(selectors.item(i).name === prev_id + '_end_ts' )
        {
            selectors.item(i).name  = new_id + '_end_ts';
            selectors.item(i).id    = new_id + '_end_ts';
        }
    }

    // Update inputs
    var inputs = new_div.getElementsByTagName('input');

    for(i = 0, len = inputs.length; i < len; i++)
    {
        if(inputs.item(i).id === prev_id + '_add')
        {
            // Set new id
            inputs.item(i).id = new_id + '_add';

            // Hide previous button
            prev_button = document.getElementById(prev_id + '_add');
            prev_button.style.display = 'none';
        }
        if(inputs.item(i).id === prev_id + '_del')
        {
            // Set new id
            inputs.item(i).id = new_id + '_del';
            // Hide previous button
            prev_button = document.getElementById(prev_id + '_del');
            prev_button.style.display = 'none';
            // Show current button
            inputs.item(i).style.display = 'inline';
        }

    }
    // Update head
    var divs = new_div.getElementsByTagName('div');
    
    for(i = 0, len = divs.length; i < len; i++)
    {
        if(divs.item(i).id === prev_id + '_head' )
        {
            // New id
            divs.item(i).id = new_id + '_head';

            // New label
            divs.item(i).innerHTML = 'Set ' + new_id.split('_')[1] + ' &gt;';
        }
    }

    // Update timestamp
    SuperposeForm.setTimestamps(new_id + '_label');
};

// Delete selected step
SuperposeForm.prototype.del = function(button) {
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
SuperposeForm.prototype.setTimestamps = function(id) {
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        var i,
            len,
            ts;

        // Calculate id
        id  = id.split('_')[0] + '_' + id.split('_')[1];

        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            // Hide Ajax spinner
            window.spinner.style.display = 'none';

            // Dates of tests
            var dates = xmlhttp.responseText.split(';');

            // Start timestamps
            var select = document.getElementById(id + '_start_ts');
            select.options.length = 0;

            for (i = 0, len = dates.length; i < len; i++){
                ts = dates[i];
                select.options[i] = new Option(ts, ts, false, false);
            }

            // End timestamps
            select = document.getElementById(id + '_end_ts');
            select.options.length = 0;
            dates.reverse();

            for (i = 0, len = dates.length; i < len; i++){
                ts = dates[i];
                select.options[i] = new Option(ts, ts, false, false);
            }
        }
    };

    var select = document.getElementById(id);
    var label = select.options[select.selectedIndex].text;
    var URI = 'dates?label=' + label;

    xmlhttp.open('GET', URI, true);
    xmlhttp.send();

    // Show Ajax spinner
    var spinner = document.getElementById('spinner');
    window.spinner.style.display = 'block';
};
// Add Ajax spinner
SuperposeForm.prototype.addSpinner = function() {
    var opts = {
            lines: 10,
            length: 6,
            width: 3,
            radius: 6,
            color: '#498a2d',
            speed: 0.8,
            trail: 80
        };
    var target = document.getElementById('spinner');
    var spinner = new Spinner(opts).spin(target);
};