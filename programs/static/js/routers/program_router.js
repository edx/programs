define([
        'backbone',
        'js/views/program_creator_view',
        'js/views/program_details_view',
        'js/views/program_list_view'
    ],
    function( Backbone, ProgramCreatorView, ProgramDetailsView, ProgramListView ) {
        'use strict';

        return Backbone.Router.extend({
            root: '/author/',

            routes: {
                '': 'programList',
                'program/new': 'programCreator',
                'program/:id': 'programDetails'
            },

            initialize: function( options ) {
                this.model = options.model;
            },

            programCreator: function() {
                if ( this.programCreatorView ) {
                    this.programCreatorView.destroy();
                }

                this.programCreatorView = new ProgramCreatorView({
                    programsModel: this.model
                });
            },

            programList: function() {
                if ( !this.programListView ) {
                    this.programListView = new ProgramListView({
                        model: this.model
                    });
                }
            },

            programDetails: function( id ) {
                var programModel = this.model.get('results').get(id);

                this.programDetailsView = new ProgramDetailsView({
                    model: programModel
                });
            },

            /**
             * Starts the router.
             */
            start: function () {
                if ( !Backbone.history.started ) {
                    Backbone.history.start({
                        pushState: true,
                        root: this.root
                    });
                }
                return this;
            }
        });
    }
);
