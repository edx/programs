define([
        'backbone',
        'backbone.validation',
        'jquery',
        'underscore',
        'js/models/organizations_model',
        'js/models/program_model',
        'text!templates/program_creator_form.underscore',
        'gettext'
    ],
    function ( Backbone, BackboneValidation, $, _, OrganizationsModel, ProgramModel, ListTpl ) {
        'use strict';

        // These are the same messages provided by Backbone.Validation,
        // marked for translation.
        // See: http://thedersen.com/projects/backbone-validation/#overriding-the-default-error-messages.
        _.extend(Backbone.Validation.messages, {
            required: gettext( '{0} is required' ),
            acceptance: gettext( '{0} must be accepted' ),
            min: gettext( '{0} must be greater than or equal to {1}' ),
            max: gettext( '{0} must be less than or equal to {1}' ),
            range: gettext( '{0} must be between {1} and {2}' ),
            length: gettext( '{0} must be {1} characters' ),
            minLength: gettext( '{0} must be at least {1} characters' ),
            maxLength: gettext( '{0} must be at most {1} characters' ),
            rangeLength: gettext( '{0} must be between {1} and {2} characters' ),
            oneOf: gettext( '{0} must be one of: gettext( {1}' ),
            equalTo: gettext( '{0} must be the same as {1}' ),
            digits: gettext( '{0} must only contain digits' ),
            number: gettext( '{0} must be a number' ),
            email: gettext( '{0} must be a valid email' ),
            url: gettext( '{0} must be a valid url' ),
            inlinePattern: gettext( '{0} is invalid' )
        });

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

                // Hook up validation.
                // See: http://thedersen.com/projects/backbone-validation/#validation-binding.
                Backbone.Validation.bind(this);

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

                // Check if the model is valid before saving. Invalid attributes are looked
                // up by name. The corresponding elements receieve an `invalid` class and a
                // `data-error` attribute. Both are removed when formerly invalid attributes
                // become valid.
                // See: http://thedersen.com/projects/backbone-validation/#isvalid.
                if ( this.model.isValid(true) ) {
                    this.model.save();
                }
            },

            destroy: function() {
                // Unhook validation.
                // See: http://thedersen.com/projects/backbone-validation/#unbinding.
                Backbone.Validation.unbind(this);

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
