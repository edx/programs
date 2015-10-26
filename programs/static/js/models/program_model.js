define([
        'backbone',
        'jquery',
        'jquery-cookie'
    ],
    function( Backbone, $ ) {
        'use strict';

        return Backbone.Model.extend({
            url: '/api/v1/programs/',

            save: function() {
                var method = '',
                    options = _.extend({validate: true, parse: true}, {
                        type: 'POST',
                        url: this.url,
                        // The API requires a CSRF token for all POST requests using session authentication.
                        headers: {'X-CSRFToken': $.cookie('programs_csrftoken')},
                        contentType: 'application/json',
                        context: this,
                        // NB: setting context fails in tests
                        success: _.bind( this.saveSuccess, this ),
                        error: _.bind( this.saveError, this )
                    });

                /**
                 * Simplified version of code from the default Backbone save function
                 * http://backbonejs.org/docs/backbone.html#section-87
                 */
                method = this.isNew() ? 'create' : 'update';

                this.sync( method, this, options);
            },

            saveError: function( jqXHR ) {
                this.trigger( 'error', jqXHR );
            },

            saveSuccess: function() {
                this.trigger( 'sync', this );
            }
        });
    }
);
