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
                'change .js-course-run-select': 'selectRun',
                'click .js-remove-run': 'removeRun'
            },

            tpl: _.template( CourseRunTpl ),

            initialize: function( options ) {
                /**
                 * Need the run model for the template, and the courseModel
                 * to keep parent view up to date with run changes
                 */
                this.courseModel = options.course;
                this.courseRuns = options.courseRuns;
                this.programStatus = options.programStatus;

                this.model.on('change', this.render, this);
                this.courseRuns.on('update', this.updateDropdown, this);

                this.$parentEl = options.$parentEl;
                this.render();
            },

            render: function() {
                var data = this.model.attributes;
                data.programStatus = this.programStatus;

                if ( !!this.courseRuns ) {
                    data.courseRuns = this.courseRuns.toJSON();
                }

                this.$el.html( this.tpl( data ) );
                this.$parentEl.append( this.$el );
            },

            // Delete this view
            destroy: function() {
                this.undelegateEvents();
                this.remove();
            },

            removeRun: function() {
                // Update run_modes array on programModel
                var startDate = this.model.get('start'),
                    courseKey = this.model.get('course_key'),
                    runs = this.courseModel.get('run_modes'),
                    updatedRuns = [];

                updatedRuns = _.filter( runs, function( obj ) {
                    return obj.start !== startDate &&
                           obj.course_key !== courseKey;
                });

                this.courseModel.set({
                    run_modes: updatedRuns
                });

                this.courseRuns.addRun(courseKey);

                this.destroy();
            },

            selectRun: function(event) {
                var id = $(event.currentTarget).val(),
                    data = _.findWhere(this.courseRuns.allRuns, {course_id: id}),
                    runs = this.courseModel.get('run_modes');

                data.course_key = id;
                this.model.set(data);
                runs.push(data);
                this.courseModel.set({run_modes: runs});
                this.courseRuns.removeRun(id);
            },

            // If a run has not been selected update the dropdown options
            updateDropdown: function() {
                if ( !this.model.get('course_key') ) {
                    this.render();
                }
            }
        });
    }
);
