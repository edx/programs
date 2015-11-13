require.config({
    baseUrl: '/static/',
    paths: {
        'afontgarde': 'bower_components/edx-pattern-library/pattern-library/js/afontgarde',
        'backbone': 'bower_components/backbone/backbone',
        // We're intentionally using code from this package's src/ directory, which includes
        // a bug fix that hasn't yet made it over to the code in dist/.
        // See: https://github.com/thedersen/backbone.validation/commit/1b949.
        'backbone.validation': 'bower_components/backbone.validation/src/backbone-validation',
        'gettext': 'js/shims/gettext',
        'jquery': 'bower_components/jquery/dist/jquery',
        'jquery-cookie': 'bower_components/jquery-cookie/jquery.cookie',
        'modernizr-custom': 'bower_components/edx-pattern-library/pattern-library/js/modernizr-custom',
        'requirejs': 'bower_components/requirejs/require',
        'text': 'bower_components/text/text',
        'underscore': 'bower_components/underscore/underscore'
    },
    shim: {
        'afontgarde' : {
            deps: ['modernizr-custom'],
            exports: 'AFontGarde'
        },
        'backbone.validation': {
            deps: ['backbone', 'underscore']
        },
        'jquery-cookie': {
            deps: ['jquery']
        }
    }
});
