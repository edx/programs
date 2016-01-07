define([
        'backbone',
        'jquery',
        'js/utils/api_config',
        'js/collections/auto_auth_collection',
        'jquery-cookie'
    ],
    function( Backbone, $, apiConfig, AutoAuthCollection ) {
        'use strict';

        return AutoAuthCollection.extend({
            allRuns: [],

            initialize: function(models, options) {
                // Ignore pagination and give me everything
                var orgStr = options.organization.display_name,
                    queries = '?org=' + orgStr + '&username=' + apiConfig.get('username') + '&page_size=1000';

                this.url = apiConfig.get('lmsBaseUrl') + 'api/courses/v1/courses/' + queries;
            },

            parse: function(data) {
                this.allRuns = data.results;

                // Because pagination is ignored just set results
                return data.results;
            },

            // Adds a run back into the model for selection
            addRun: function(id) {
                var courseRun = _.findWhere( this.allRuns, { course_id: id });

                this.create(courseRun);
            },

            // Removes a run from the model for selection
            removeRun: function(id) {
                var courseRun = this.where({course_id: id});

                this.remove(courseRun);
            }
        });
    }
);
