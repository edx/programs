define([
        'backbone',
        'jquery',
        'underscore',
        'js/models/organizations_model',
        'js/models/program_model',
        'text!templates/program_creator_form.underscore',
        'gettext'
    ],
    function ( Backbone, $, _, OrganizationsModel, ProgramModel, ListTpl ) {
        'use strict';

        return Backbone.View.extend({
            parentEl: '.js-program-admin',

            events: {
                'click .js-create-program': 'createProgram',
                'click .js-abort-view': 'abort'
            },

            tpl: _.template( ListTpl ),

            initialize: function( options ) {
                this.$parentEl = $( this.parentEl );

                this.model = new ProgramModel();
                this.model.on( 'sync', this.saveSuccess, this );
                this.model.on( 'error', this.saveError, this );

                this.programsModel = options.programsModel;
                this.programsModel.on( 'sync', this.goToListView, this );

                this.organizations = new OrganizationsModel();
                this.organizations.on( 'sync', this.render, this );
                this.organizations.fetch();
            },

            render: function() {
                this.$el.html(
                    this.tpl( {
                        orgs: this.organizations.get('results')
                    })
                );

                this.$parentEl.html( this.$el );
            },

            abort: function() {
                this.goToListView();
            },

            createProgram: function( event ) {
                var data = this.getData();

                event.preventDefault();
                this.model.set( data );
                this.model.save();
            },

            destroy: function() {
                this.undelegateEvents();
                this.remove();
            },

            getData: function() {
                return {
                    name: this.$el.find( '.program-name' ).val(),
                    subtitle: this.$el.find( '.program-subtitle' ).val(),
                    category: this.$el.find( '.program-type' ).val(),
                    organization: [{
                        key: this.$el.find( '.program-org' ).val()
                    }]
                };
            },

            goToListView: function() {
                Backbone.history.navigate( '', { trigger: true } );
                this.destroy();
            },

            // TODO: add user messaging to show errors
            saveError: function( jqXHR ) {
                console.log( 'saveError: ', jqXHR );
            },

            saveSuccess: function() {
                this.programsModel.getList();
            }
        });
    }
);
