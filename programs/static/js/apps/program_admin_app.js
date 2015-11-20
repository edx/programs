(function() {
    'use strict';

    /**
     * Allows for rapid toggling between app version locally
     * i.e. just swap out the file name in the require array
     */
    require([
            'js/views/program_admin_app_view_core'
        ],
        function( ProgramAdminApp ) {
            return new ProgramAdminApp();
        }
    );
})();
