define([
        'js/views/program_admin_app_view_core',
        'js/routers/dev_app_program_router',
        'js/utils/api_config'
    ],
    function( ProgramAdminAppCore, ProgramRouter, apiConfig ) {
        'use strict';

        return ProgramAdminAppCore.extend({
            initialize: function() {
                var apiUrl = this.$el.data('api-url'),
                    authUrl = this.$el.data('auth-url'),
                    homeUrl = this.$el.data('home-url');

                apiConfig.set({
                    baseUrl: apiUrl,
                    authUrl: authUrl
                });

                this.app = new ProgramRouter({
                    homeUrl: homeUrl
                });
                this.app.start();
            }
        });
    }
);
