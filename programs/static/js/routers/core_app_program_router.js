define([
        'backbone',
        'js/views/program_creator_view',
        'js/views/program_details_view',
        'js/views/program_list_view',
        'js/models/pagination_model',
        'js/models/program_model'
    ],
    function( Backbone, ProgramCreatorView, ProgramDetailsView,
              ProgramListView, ProgramsListModel, ProgramModel ) {
        'use strict';

        return Backbone.Router.extend({
            root: '/program/',

            routes: {
                'new': 'programCreator',
                ':id': 'programDetails'
            },

            initialize: function( options ) {
                this.homeUrl = options.homeUrl;
            },

            goHome: function() {
                window.location.href = this.homeUrl;
            },

            loadProgramDetails: function() {
                this.programDetailsView = new ProgramDetailsView({
                    model: this.programModel
                });
            },

            programCreator: function() {
                if ( this.programCreatorView ) {
                    this.programCreatorView.destroy();
                }

                this.programCreatorView = new ProgramCreatorView({
                    router: this
                });
            },

            programDetails: function( id ) {
                 this.programModel = new ProgramModel({
                    id: id
                });

                this.programModel.on( 'sync', this.loadProgramDetails, this );
                this.programModel.fetch();
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
