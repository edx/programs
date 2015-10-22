define([
        'backbone',
        'js/views/program_details_view',
        'js/views/program_list_view'
    ],
    function( Backbone, ProgramDetailsView, ProgramListView ) {
        'use strict';

        return Backbone.Router.extend({
            root: '/author/',

            routes: {
                '': 'programList',
                'program/:id': 'programDetails'
            },

            initialize: function( options ) {
                this.model = options.model;
            },

            // TODO: prevent zombie views
            programList: function() {
                this.programList = new ProgramListView({
                    model: this.model
                });
            },

            programDetails: function( id ) {
                var programModel = this.model.get('results').get(id);

                this.programDetails = new ProgramDetailsView({
                    model: programModel
                });
            },

            /**
             * Starts the router.
             */
            start: function () {
                Backbone.history.start({pushState: true, root: this.root});
                return this;
            }
        });
    }
);
