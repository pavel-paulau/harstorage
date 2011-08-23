/* See license.txt for terms of usage */

require.def("core/trace", [
],

function() {

//*************************************************************************************************

var Trace = {
    log: function(){},
    error: function(){},
    exception: function(){},
    time: function(){},
    timeEnd: function(){}
};

if (typeof(console) == "undefined")
    return Trace;


return Trace;

//*************************************************************************************************
});

