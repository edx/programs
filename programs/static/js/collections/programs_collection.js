define([
        'backbone',
        'jquery',
        'js/models/program_model'
    ],
    function( Backbone, $, ProgramModel ) {
        'use strict';

        return Backbone.Collection.extend({
            model: ProgramModel
        });
    }
);
