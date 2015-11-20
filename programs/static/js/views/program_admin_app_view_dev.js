define([
        'js/views/program_admin_app_view_core',
        'js/routers/dev_app_program_router'
    ],
    function( ProgramAdminAppCore, ProgramRouter) {
        'use strict';

        return ProgramAdminAppCore.extend({
            initialize: function() {
                var home = this.$el.data('home-url');

                this.app = new ProgramRouter({
                    homeUrl: home
                });
                this.app.start();
            }
        });
    }
);
