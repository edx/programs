/* jshint asi:true, expr:true */
({
    mainConfigFile: 'programs/static/js/config.js',
    baseUrl: 'programs/static',
    dir: 'programs/static/build',
    removeCombined: true,
    findNestedDependencies: true,

    // Disable all optimization. django-compressor will handle that for us.
    optimizeCss: false,
    optimize: 'none',
    normalizeDirDefines: 'all',
    skipDirOptimize: true,

    preserveLicenseComments: true,
    modules: [
        {
            name: 'js/common'
        },
        {
            name: 'js/apps/program_admin_app',
            exclude: ['js/common']
        }
    ]
})
