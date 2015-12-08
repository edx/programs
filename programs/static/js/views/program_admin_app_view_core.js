(function() {
    'use strict';

    define([
            'backbone',
            'js/routers/core_app_program_router',
            'js/utils/api_config'
        ],
        function( Backbone, ProgramRouter, apiConfig ) {
            return Backbone.View.extend({
                el: '.js-program-admin',

                events: {
                    'click .js-app-click': 'navigate'
                },

                initialize: function() {
                    var apiUrl = this.$el.data('api-url'),
                        authUrl = this.$el.data('auth-url'),
                        homeUrl = this.$el.data('home-url');

                    apiConfig.set({
                        baseUrl: apiUrl,
                        authUrl: authUrl
                    });

                    this.app = new ProgramRouter({
                        homeUrl: homeUrl
                    });
                    this.app.start();
                },

                /**
                 * Navigate to a new page within the app.
                 *
                 * Attempts to open the link in a new tab/window behave as the user expects, however the app
                 * and data will be reloaded in the new tab/window.
                 *
                 * @param {Event} event - Event being handled.
                 * @returns {boolean} - Indicates if event handling succeeded (always true).
                 */
                navigate: function (event) {
                    var url = $(event.target).attr('href').replace( this.app.root, '' );

                    /**
                     * Handle the cases where the user wants to open the link in a new tab/window.
                     * event.which === 2 checks for the middle mouse button (https://api.jquery.com/event.which/)
                     */
                    if ( event.ctrlKey || event.shiftKey || event.metaKey || event.which === 2 ) {
                        return true;
                    }

                    // We'll take it from here...
                    event.preventDefault();

                    // Process the navigation in the app/router.
                    if ( url === Backbone.history.getFragment() && url === '' ) {
                        /**
                         * Note: We must call the index directly since Backbone
                         * does not support routing to the same route.
                         */
                        this.app.index();
                    } else {
                        this.app.navigate( url, { trigger: true } );
                    }
                }
            });
        }
    );
})();
