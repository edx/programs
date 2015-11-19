define([
        'backbone',
        'jquery',
        'underscore',
        'js/utils/constants',
        'text!templates/confirm_modal.underscore',
        'gettext'
    ],
    function( Backbone, $, _, constants, ModalTpl ) {
        'use strict';

        return Backbone.View.extend({
            events: {
                'click .js-cancel': 'destroy',
                'click .js-confirm': 'confirm',
                'keydown': 'handleKeydown'
            },

            tpl: _.template( ModalTpl ),

            initialize: function( options ) {
                this.$parentEl = $( options.parentEl );
                this.callback = options.callback;
                this.content = options.content;
                this.render();
            },

            render: function() {
                this.$el.html( this.tpl( this.content ) );
                this.$parentEl.html( this.$el );
                this.postRender();
            },

            postRender: function() {
                this.$el.find('.js-focus-first').focus();
            },

            confirm: function() {
                this.callback();
                this.destroy();
            },

            destroy: function() {
                this.undelegateEvents();
                this.remove();
                this.$parentEl.html('');
            },

            handleKeydown: function( event ) {
                var keyCode = event.keyCode;

                if ( keyCode === constants.keyCodes.esc ) {
                    this.destroy();
                }
            }
        });
    }
);
