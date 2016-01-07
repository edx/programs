define([
        'js/views/program_admin_app_view_core',
        'js/routers/dev_app_program_router',
        'js/utils/api_config'
    ],
    function( ProgramAdminAppCore, ProgramRouter, apiConfig ) {
        'use strict';

        return ProgramAdminAppCore.extend({
            initialize: function() {
                apiConfig.set({
                    lmsBaseUrl: this.$el.data('lms-base-url'),
                    programsApiUrl: this.$el.data('programs-api-url'),
                    authUrl: this.$el.data('auth-url'),
                    username: this.$el.data('username')
                });

                this.app = new ProgramRouter({
                    homeUrl: this.$el.data('home-url')
                });
                this.app.start();
            }
        });
    }
);
