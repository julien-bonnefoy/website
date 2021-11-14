requirejs.config({
    paths: {
        jquery: 'jquery.slim.min.js',
        bootstrap: 'bootstrap.min.js',
        popper: "popper.min.js",
        plotly: "plotly.min.js"
    },
    shim: {
        'bootstrap': {
            deps:['jquery', 'popper']
        },
    }
});

require(['jquery', 'popper', 'plotly', 'bootstrap'], function($) {
    console.log($.fn)
});