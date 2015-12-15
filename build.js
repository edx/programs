/* jshint asi:true, expr:true */
({
    // For documentation of the directives in this build file, refer to
    // the example require.js build file located at:
    // https://github.com/jrburke/r.js/blob/master/build/example.build.js

    // See: https://github.com/jrburke/r.js/blob/master/build/example.build.js#L27-L37
    mainConfigFile: 'programs/static/js/config.js',

    // See: https://github.com/jrburke/r.js/blob/master/build/example.build.js#L21-L25
    baseUrl: 'programs/static',

    // See: https://github.com/jrburke/r.js/blob/master/build/example.build.js#L59-L62
    dir: 'programs/static/build',

    // See: https://github.com/jrburke/r.js/blob/master/build/example.build.js#L341-L347
    findNestedDependencies: true,

    // See: https://github.com/jrburke/r.js/blob/master/build/example.build.js#L80-L91
    // See also: http://jrburke.com/2014/02/16/requirejs-2.1.11-released/
    wrapShim: true,

    // See: https://github.com/jrburke/r.js/blob/master/build/example.build.js#L208-L220
    optimizeCss: 'standard',

    // See: https://github.com/jrburke/r.js/blob/master/build/example.build.js#L99-L110
    optimize: 'uglify2',

    // See: https://github.com/jrburke/r.js/blob/master/build/example.build.js#L133-L152
    normalizeDirDefines: 'all',

    // See: https://github.com/jrburke/r.js/blob/master/build/example.build.js#L112-L119
    skipDirOptimize: true,

    // See: https://github.com/jrburke/r.js/blob/master/build/example.build.js#L349-L351
    removeCombined: true,

    // https://github.com/jrburke/r.js/blob/master/build/example.build.js#L511-L521
    preserveLicenseComments: true,

    // https://github.com/jrburke/r.js/blob/master/build/example.build.js#L353-L357
    modules: [
        {
            name: 'js/common'
        },
        {
            name: 'js/apps/program_admin_app_core',
            exclude: ['js/common']
        },
        {
            name: 'js/apps/program_admin_app_dev',
            exclude: ['js/common']
        },
        {
            name: 'js/apps/program_admin_app',
            exclude: ['js/common']
        },
    ]
})
