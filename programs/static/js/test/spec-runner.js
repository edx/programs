var specs = [],
    config = {};

// You can automatically get the test files using karma's configs
for (var file in window.__karma__.files) {
    if (/js\/test\/specs\/.*spec\.js$/.test(file)) {
        specs.push(file);
    }
}

// This is where karma puts the files.
config.baseUrl = '/base/programs/static/';

// Karma lets you list the test files here.
config.deps = specs;
config.callback = window.__karma__.start;

requirejs.config(config);
