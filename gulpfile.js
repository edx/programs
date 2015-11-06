'use strict';

var del = require('del'),
    gulp = require('gulp'),
    jscs = require('gulp-jscs'),
    jshint = require('gulp-jshint'),
    KarmaServer = require('karma').Server,
    sass = require('gulp-sass'),
    path = require('path'),
    paths = {
        karmaConf: 'karma.conf.js',
        lint: [
            'build.js',
            'gulpfile.js',
            'programs/static/js/**/*.js',
            'programs/static/js/test/**/*.js',
            '!programs/bower_components/**/*.js'
        ],
        spec: [
            'programs/static/js/**/*.js',
            'programs/static/js/test/**/*.js',
            'programs/static/templates/**/*.js'
        ],
        styles: {
            src: 'programs/static/sass/**/*.scss',
            dest: 'programs/static/css/'
        }
    };

/**
 * Runs the JS unit tests
 */
gulp.task('test', function (cb) {
    new KarmaServer({
        configFile: path.resolve('karma.conf.js')
    }, cb).start();
});

/**
 * Runs the JSHint linter.
 *
 * http://jshint.com/about/
 */
gulp.task('lint', function () {
    return gulp.src(paths.lint)
        .pipe(jshint())
        .pipe(jshint.reporter('default'))
        .pipe(jshint.reporter('fail'));
});

/**
 * Runs the JavaScript Code Style (JSCS) linter.
 *
 * http://jscs.info/
 */
gulp.task('jscs', function () {
    return gulp.src(paths.lint)
        .pipe(jscs());
});

/**
 * Compiles CSS from src Sass files
 * first it removes the output folder to start clean
 */
gulp.task('css', function() {
    del([ paths.styles.dest ])
        .then( function() {
            return gulp.src( paths.styles.src )
                .pipe( sass().on( 'error', sass.logError ) )
                .pipe( gulp.dest( paths.styles.dest ) );
        });
});

/**
 * Monitors the source and test files, running tests
 * and linters when changes detected.
 */
gulp.task('watch', function () {
    gulp.watch(paths.spec, ['test', 'lint', 'jscs']);
});

gulp.task('default', ['test', 'css']);
