(function() {
    'use strict';

    require([
            'js/views/program_list_view'
        ],
        function( ProgramListView ) {
            return new ProgramListView();
        }
    );
})();
