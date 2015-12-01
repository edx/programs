define([
        'js/models/auto_auth_model'
    ],
    function( AutoAuthModel ) {
        'use strict';

        return AutoAuthModel.extend({
            defaults: [
                {
                    name: 'Course 1',
                    id: '001'
                }, {
                    name: 'Course 2',
                    id: '002'
                }, {
                    name: 'Course 3',
                    id: '003'
                }, {
                    name: 'Course 4',
                    id: '004'
                }
            ]
        });
    }
);
