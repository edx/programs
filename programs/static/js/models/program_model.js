define([
        'backbone',
        'jquery',
        'jquery-cookie'
    ],
    function( Backbone, $ ) {
        'use strict';

        return Backbone.Model.extend({
            url: '/api/v1/programs/',

            // Backbone.Validation rules.
            // See: http://thedersen.com/projects/backbone-validation/#configure-validation-rules-on-the-model.
            validation: {
                name: {
                    required: true,
                    maxLength: 64
                },
                subtitle: {
                    // The underlying Django model does not require a subtitle.
                    maxLength: 255
                },
                category: {
                    required: true,
                    // XSeries is currently the only valid Program type.
                    oneOf: ['xseries']
                },
                organization: 'validateOrganization',
                marketing_slug: {
                    // The underlying Django model does not require a marketing_slug.
                    maxLength: 255
                }
            },

            validateOrganization: function(orgArray) {
                // The array passed to this method contains a single object representing
                // the selected organization; the object contains the organization's key.
                // In the future, multiple organizations might be associated with a program.
                var i;

                for (i = 0; i < orgArray.length; i++) {
                    if ( orgArray[i].key === 'false' ) {
                        return gettext('Please select a valid organization.');
                    }
                }
            },

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
