define([
        'afontgarde'
    ],
    function( AFontGarde ) {
        'use strict';

        /**
         * Adds the 'edx-icons' class to the DOM's HTML element
         * if the icon fonts successfully load
         */
        return new AFontGarde('edx-icons', {
            // Check a few random icons to see if our font loads
            glyphs: '\uE621\uE622\uE623'
        });
    }
);
