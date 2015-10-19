define([
        'backbone',
        'jquery',
        'underscore',
        'js/models/pagination_model',
        'text!templates/program_list.underscore'
    ],
    function ( Backbone, $, _, ProgramsModel, ListTpl ) {
        'use strict';

        return Backbone.View.extend({
            el: '.js-program-admin',

            tpl: _.template( ListTpl ),

            initialize: function() {
                this.model = new ProgramsModel();
                this.model.on( 'sync', this.render, this );
                this.model.getList();
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
