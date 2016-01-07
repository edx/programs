define([
        'js/utils/api_config',
        'js/models/auto_auth_model'
    ],
    function( apiConfig, AutoAuthModel ) {
        'use strict';

        return AutoAuthModel.extend({

            initialize: function() {
                this.urlRoot = apiConfig.get('programsApiUrl') + 'organizations/';
            }

        });
    }
);
