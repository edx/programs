(function() {
    'use strict';

    require([
            'backbone',
            'js/models/pagination_model',
            'js/routers/program_router'
        ],
        function( Backbone, ProgramsModel, ProgramRouter ) {
            var ProgramAdminApp = Backbone.View.extend({
                el: '.js-program-admin',

                events: {
                    'click .js-app-click': 'navigate'
                },

                initialize: function() {
                    this.model = new ProgramsModel();
                    this.model.once( 'sync', this.start, this );
                    this.model.getList();
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
                },

                start: function() {
                    this.app = new ProgramRouter({
                        model: this.model
                    });
                    this.app.start();

                    // Listen for additions/deletions from results
                    this.model.on( 'change:results', this.model.fetch, this );
                }
            });

            return new ProgramAdminApp();
        }
    );
})();
