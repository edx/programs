require.config({
    baseUrl: '/static/',
    paths: {
        'backbone': 'bower_components/backbone/backbone',
        'gettext': 'js/shims/gettext',
        'jquery': 'bower_components/jquery/dist/jquery',
        'jquery-cookie': 'bower_components/jquery-cookie/jquery.cookie',
        'requirejs': 'bower_components/requirejs/require',
        'text': 'bower_components/text/text',
        'underscore': 'bower_components/underscore/underscore'
    },
    shim: {
        'jquery-cookie': {
            deps: ['jquery']
        }
    }
});
