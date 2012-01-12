/*
 * Name space
 */
var HARSTORAGE = HARSTORAGE || {};

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