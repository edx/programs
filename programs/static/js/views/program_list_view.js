define([
        'backbone',
        'jquery',
        'underscore',
        'text!templates/program_list.underscore'
    ],
    function ( Backbone, $, _, ListTpl ) {
        'use strict';

        return Backbone.View.extend({
            el: '.js-program-admin',

            tpl: _.template( ListTpl ),

            initialize: function() {
                this.render();
            },

            render: function() {
                if ( this.model.get('count') > 0 ) {
                    this.$el.html(
                        this.tpl( {
                            programs: this.model.get('results')
                        })
                    );
                }
            }
        });
    }
);
