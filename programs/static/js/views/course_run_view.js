define([
        'backbone',
        'jquery',
        'underscore',
        'text!templates/course_run.underscore',
        'js/shims/edx-icons'
    ],
    function ( Backbone, $, _, CourseRunTpl ) {
        'use strict';

        return Backbone.View.extend({
            events: {
                'click .js-remove-run': 'removeRun'
            },

            tpl: _.template( CourseRunTpl ),

            initialize: function( options ) {
                /**
                 * Need the run data for the template, but the model
                 * to keep parent view up to date with run changes
                 */
                this.data = options.data;
                this.data.programStatus = this.model.get('programStatus');

                // Temporary hack
                // ===============
                // TODO: Remove this once API is updated to include start_date
                this.data.start_date = this.data.start_date || 'January 01, 2016';

                this.$parentEl = options.$parentEl;
                this.render();
            },

            render: function() {
                this.$el.html( this.tpl( this.data ) );
                this.$parentEl.append( this.$el );
            },

            // Delete this view
            destroy: function() {
                this.undelegateEvents();
                this.remove();
            },

            removeRun: function() {
                // Update run_modes array on model
                var startDate = this.data.start_date,
                    courseKey = this.data.course_key,
                    runs = this.model.get('run_modes'),
                    updatedRuns = _.filter( runs, function( obj ) {
                        return obj.start_date !== startDate &&
                               obj.course_key !== courseKey;
                    });

                this.model.set({
                    run_modes: updatedRuns
                });

                this.destroy();
            }
        });
    }
);
