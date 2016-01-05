define([
        'afontgarde'
    ],
    function( AFontGarde ) {
        'use strict';

        return new AFontGarde('edx-icons', {
            // Check a few random icons to see if our font loads
            glyphs: '\uE621\uE622\uE623',
            /**
             * Adds the 'uxpl-icons' class to the programs IDA container
             * if the icon fonts successfully load
             */
            success: function() {
                document.getElementById('content').className += ' uxpl-icons';
            }
        });
    }
);
