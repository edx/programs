define([
        'backbone',
        'backbone.validation',
        'jquery',
        'underscore',
        'js/models/course_model',
        'js/models/course_run_model',
        'js/models/pagination_model',
        'js/models/program_model',
        'js/views/course_run_view',
        'text!templates/course_details.underscore',
        'gettext',
        'js/utils/validation_config'
    ],
    function( Backbone, BackboneValidation, $, _, CourseModel, CourseRunModel,
              ProgramsModel, ProgramModel, CourseRunView, ListTpl ) {
        'use strict';

        return Backbone.View.extend({
            parentEl: '.js-course-list',

            className: 'course-details',

            events: {
                'click .js-remove-course': 'destroy',
                'click .js-select-course': 'setCourse',
                'click .js-add-course-run': 'addCourseRun'
            },

            tpl: _.template( ListTpl ),

            // For managing subViews
            courseRunViews: [],

            initialize: function( options ) {
                this.model = new CourseModel();
                Backbone.Validation.bind( this );
                this.$parentEl = $( this.parentEl );

                this.courseRuns = options.courseRuns;
                this.programModel = options.programModel;
                
                if ( options.courseData ) {
                    this.model.set(options.courseData);
                } else {
                    /**
                     * TODO: Debug why a new model is inheriting the run_modes from
                     * the program's first course. It will be much easier to debug
                     * during ECOM-3046 so I will tackle it then
                     */
                    this.model.set({run_modes: []});
                }
                // Need a unique value for field ids so using model cid
                this.model.set({cid: this.model.cid});

                this.render();
            },

            render: function() {
                this.$el.html( this.tpl( this.formatData() ) );
                this.$parentEl.append( this.$el );
                this.postRender();
            },

            postRender: function() {
                var runs = this.model.get('run_modes');
                if ( runs && runs.length > 0 ) {
                    this.addCourseRuns();
                }
            },

            addCourseRun: function(event) {
                var $runsContainer = this.$el.find('.js-course-runs'),
                    runModel = new CourseRunModel(),
                    runView;

                event.preventDefault();

                runModel.set({course_key: undefined});

                runView = new CourseRunView({
                    model: runModel,
                    course: this.model,
                    courseRuns: this.courseRuns,
                    programStatus: this.programModel.get('status'),
                    $parentEl: $runsContainer
                });

                this.courseRunViews.push( runView );
            },

            addCourseRuns: function() {
                // Create run views
                var runs = this.model.get('run_modes'),
                    $runsContainer = this.$el.find('.js-course-runs');

                _.each( runs, function( run ) {
                    var runModel = new CourseRunModel(),
                        runView;

                    runModel.set(run);

                    runView = new CourseRunView({
                        model: runModel,
                        course: this.model,
                        courseRuns: this.courseRuns,
                        programStatus: this.programModel.get('status'),
                        $parentEl: $runsContainer
                    });

                    this.courseRunViews.push( runView );

                    return runView;
                }.bind(this) );
            },

            // Delete this view
            destroy: function() {
                Backbone.Validation.unbind(this);
                this.destroyChildren();
                this.undelegateEvents();
                this.remove();
            },

            destroyChildren: function() {
                var runs = this.courseRunViews;

                _.each( runs, function( run ) {
                    run.removeRun();
                });
            },

            // Format data to be passed to the template
            formatData: function() {
                var data = $.extend( {}, 
                    { courseRuns: this.courseRuns.models },
                    _.omit( this.programModel.toJSON(), 'run_modes'),
                    this.model.toJSON()
                );

                return data;
            },

            setCourse: function( event ) {
                var $form = this.$('.js-course-form'),
                    title = $form.find('.display-name').val(),
                    key = $form.find('.course-key').val();

                event.preventDefault();

                this.model.set({
                    display_name: title,
                    key: key,
                    organization: this.programModel.get('organizations')[0]
                });

                if ( this.model.isValid(true) ) {
                    this.update();
                    this.addCourseRuns();
                }
            },

            update: function() {
                this.$el.html( this.tpl( this.formatData()  ) );
            }
        });
    }
);
