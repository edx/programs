define([
        'backbone'
    ],
    function( Backbone ) {
        'use strict';

        return Backbone.Model.extend({
            defaults: {
                'base_url': 'http://127.0.0.1:8009/api/v1/',
                'auth_url' : 'http://127.0.0.1:8001/programs/id_token/',
                'id_token' : ''
            }
        });
    }
);
