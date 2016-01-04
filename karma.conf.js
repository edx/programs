// Karma configuration
// Generated on Tue Jul 21 2015 10:10:16 GMT-0400 (EDT)

module.exports = function(config) {
  config.set({

    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: '',


    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine-jquery', 'jasmine', 'requirejs', 'sinon'],


    // list of files / patterns to load in the browser
	files: [
      {pattern: 'programs/static/vendor/**/*.js', included: false},
      {pattern: 'programs/static/bower_components/**/*.js', included: false},
      {pattern: 'programs/static/js/**/*.js', included: false},
      {pattern: 'programs/static/css/*.css', included: false},
      {pattern: 'programs/static/templates/**/*.underscore', included: false},
      {pattern: 'programs/static/templates/**/*.html', included: false},
      'programs/static/js/config.js',
      'programs/static/js/test/spec-runner.js'
    ],

    // list of files to exclude
    exclude: [],

    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: {
        'programs/static/js/!(test|shims)/**/*.js': ['coverage']
    },

    // enabled plugins
    plugins:[
       'karma-jasmine',
       'karma-jasmine-jquery',
       'karma-requirejs',
       'karma-firefox-launcher',
       'karma-coverage',
       'karma-spec-reporter',
       'karma-sinon'
   ],

    // Karma coverage config
    coverageReporter: {
        reporters: [
            {type: 'text'},
            { type: 'lcov', subdir: 'report-lcov' }
        ]
    },

    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['spec', 'coverage'],

    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: false,


    // start these browsers
    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
    browsers: ['Firefox'],


    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: true
  })
}
