define([
        'backbone'
    ],
    function( Backbone ) {
        'use strict';

        return Backbone.Model.extend({
            urlRoot: '/api/v1/organizations/'
        });
    }
);
