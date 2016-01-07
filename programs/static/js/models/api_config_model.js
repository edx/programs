define([
        'backbone'
    ],
    function( Backbone ) {
        'use strict';

        return Backbone.Model.extend({
            defaults: {
                username: '',
                lmsBaseUrl: 'http://127.0.0.1:8001/',
                programsApiUrl: 'http://127.0.0.1:8004/',
                authUrl: 'http://127.0.0.1:8001/programs/id_token/',
                idToken: ''
            }
        });
    }
);
