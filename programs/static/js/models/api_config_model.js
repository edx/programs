define([
        'backbone'
    ],
    function( Backbone ) {
        'use strict';

        return Backbone.Model.extend({
            defaults: {
                baseUrl: 'http://127.0.0.1:8004/api/v1/',
                authUrl: 'http://127.0.0.1:8001/programs/id_token/',
                idToken: ''
            }
        });
    }
);
