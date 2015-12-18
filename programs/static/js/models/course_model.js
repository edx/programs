define([
        'backbone',
        'jquery',
        'js/utils/api_config',
        'js/models/auto_auth_model',
        'jquery-cookie'
    ],
    function( Backbone, $, apiConfig, AutoAuthModel ) {
        'use strict';

        return AutoAuthModel.extend({

            validation: {
                key: {
                    required: true,
                    maxLength: 64
                },
                display_name: {
                    required: true,
                    maxLength: 128
                }
            },

            defaults: {
                display_name: false,
                key: false,
                organization: [],
                run_modes: []
            }
        });
    }
);
