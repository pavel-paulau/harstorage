/*
 * Name space
 */
var HARSTORAGE = HARSTORAGE || {};

/*
 * Cookies
 */
HARSTORAGE.create_cookie = function(name, value) {
    "use strict";

    document.cookie = name + "=" + value + ";" +
                      "expires=Wed, 1 Jan 2014 00:00:00 UTC;" +
                      "path=/";
};

HARSTORAGE.read_cookie = function(name) {
    "use strict";

    var nameEQ = name + "=";
    var cookies = document.cookie.split(";");

    for (var i=0; i < cookies.length; i++) {
        var cookie = cookies[i];
        while (cookie.charAt(0) === " ") {
            cookie = cookie.substring(1, cookie.length);
        }
        if (cookie.indexOf(nameEQ) === 0) {
            return cookie.substring(nameEQ.length, cookie.length);
        }
    }

    return null;
};

/*
 * View Preferences Menu
 */
HARSTORAGE.view_preferences = function() {
    "use strict";

    // Read preference from Cookie
    var theme = HARSTORAGE.read_cookie("chartTheme");

    // If preference is found - update form
    if (theme) {
        var theme_list = document.getElementById("theme-list");

        var len = theme_list.length;

        for (var i=0; i < len; i++ ) {
            if (theme_list[i].value === theme) {
                theme_list[i].checked = true;
                break;
            }
        }
    }

    // Display preference menu
    var menu = document.getElementById("preferences");
    
    if (menu.style.display === "none" || menu.style.display === "") {
        menu.style.display = "block";
    } else {
        menu.style.display = "none";
    }
};

/*
 * Update Preferences
 */
HARSTORAGE.update_preferences = function() {
    "use strict";

    // Look up for selected theme
    var theme_list = document.getElementById("theme-list");

    var len = theme_list.length;

    for (var i=0; i < len; i++ ) {
        if (theme_list[i].checked === true) {
            HARSTORAGE.create_cookie("chartTheme", theme_list[i].value);
            break;
        }
    }

    // Refresh current window
    window.location.reload();    
};

/*
 * Chart colors from theme
 */
HARSTORAGE.Colors = function() {
    "use strict";

    // Colors for Y Axis labels
    var theme = HARSTORAGE.read_cookie("chartTheme");

    if (theme === "dark-green" || !theme) {
        return [
            "#DDDF0D",
            "#55BF3B",
            "#DF5353",
            "#7798BF",
            "#6AF9C4",
            "#DB843D",
            "#EEAAEE",
            "#669933",
            "#CC3333",
            "#FF9944",
            "#996633",
            "#4572A7",
            "#80699B",
            "#92A8CD",
            "#A47D7C",
            "#9A48C9",
            "#C99A48",
            "#879D79"
        ];
    } else {
        return [
            "#669933",
            "#CC3333",
            "#FF9944",
            "#996633",
            "#4572A7",
            "#80699B",
            "#92A8CD",
            "#EEAAEE",
            "#A47D7C",
            "#DDDF0D",
            "#55BF3B",
            "#DF5353",
            "#7798BF",
            "#6AF9C4",
            "#DB843D",
            "#9A48C9",
            "#C99A48",
            "#879D79"
        ];
    }
};

/*
 * Spinner options
 */
HARSTORAGE.SpinnerOpts = {
    lines: 10,
    length: 6,
    width: 3,
    radius: 6,
    color: "#498a2d",
    speed: 0.8,
    trail: 80
};