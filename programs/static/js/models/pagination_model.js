define([
        'backbone',
        'jquery',
        'js/collections/programs_collection'
    ],
    function( Backbone, $, ProgramsCollection ) {
        'use strict';

        return Backbone.Model.extend({
            urlRoot: '/api/v1/programs/',

            initialize: function() {
                this.setHeaders();
            },

            getList: function() {
                $.ajax({
                    type: 'GET',
                    url: this.urlRoot,
                    headers: this.headers,
                    contentType: 'application/json; charset=utf-8',
                    context: this,
                    success: function( data ) {
                        var programsCollection = new ProgramsCollection();
                        programsCollection.set(data.results);
                        data.results = programsCollection;

                        this.set( data );
                        this.trigger( 'sync', this );
                    },
                    error: function( jqXHR ) {
                        console.log( 'error: ', jqXHR );
                    }
                });
            },

            setHeaders: function() {
                this.headers = {};
            }
        });
    }
);
