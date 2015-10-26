define([
        'backbone',
        'jquery',
        'underscore',
        'js/models/pagination_model',
        'js/models/program_model',
        'js/views/course_run_view',
        'text!templates/course_details.underscore',
        'gettext'
    ],
    function( Backbone, $, _, ProgramsModel, ProgramModel,
              CourseRunView, ListTpl ) {
        'use strict';

        return Backbone.View.extend({
            parentEl: '.js-course-list',

            className: 'course-details',

            events: {
                'change .js-course-select': 'setCourse',
                'click .js-remove-course': 'destroy'
            },

            tpl: _.template( ListTpl ),

            // For managing subViews
            courseRuns: [],

            initialize: function( options ) {
                this.model = new ProgramModel();
                this.$parentEl = $( this.parentEl );

                // Data passed in because it is not an actual model
                if ( options.data ) {
                    this.model.set( options.data );
                } else {
                    this.courseList = options.courseList.toJSON();
                    this.setDefaultModel();
                }

                this.model.on('change:display_name', this.update, this);
                this.render();
            },

            render: function() {
                this.$el.html( this.tpl( this.model.toJSON() ) );
                this.$parentEl.append( this.$el );
                this.postRender();
            },

            postRender: function() {
                var runs = this.model.get('run_modes');

                if ( runs && runs.length > 0 ) {
                    this.addCourseRuns();
                }
            },

            addCourseRuns: function() {
                // Create run views
                var runs = this.model.get('run_modes'),
                    $runsContainer = this.$el.find('.js-course-runs');

                _.each( runs, function( run ) {
                    var runView = new CourseRunView({
                        model: this.model,
                        data: run,
                        $parentEl: $runsContainer
                    });

                    this.courseRuns.push( runView );

                    return runView;
                }.bind(this) );
            },

            // Delete this view
            destroy: function() {
                this.destroyChildren();
                this.undelegateEvents();
                this.remove();
            },

            destroyChildren: function() {
                var runs = this.courseRuns;

                _.each( runs, function( run ) {
                    run.destroy();
                });
            },

            setCourse: function( event ) {
                var $select = $(event.currentTarget),
                    value = $select.val();

                this.model.set({
                    display_name: value,
                    key: 'added-course-key',
                    organization: {
                        display_name: 'added-course-org-display-name',
                        key: 'added-course-org-key',
                    },
                    run_modes: [
                        {
                            course_key: 'course-v1:edX+DemoX+Demo_Course',
                            mode_slug: 'honor',
                            sku: null,
                            start_date: 'May 23, 2015'
                        }, {
                            course_key: 'course-v1:edX+DemoX+Demo_Course',
                            mode_slug: 'honor',
                            sku: null,
                            start_date: 'August 01, 2015'
                        }, {
                            course_key: 'course-v1:edX+DemoX+Demo_Course',
                            mode_slug: 'honor',
                            sku: null,
                            start_date: 'December 11, 2015'
                        }
                    ]
                });

                this.addCourseRuns();
            },

            setDefaultModel: function() {
                this.model.set({
                    display_name: false,
                    courseList: this.courseList
                });
            },

            update: function() {
                this.$el.html( this.tpl( this.model.toJSON() ) );
            }
        });
    }
);
