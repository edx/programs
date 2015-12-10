define([
        'backbone',
        'backbone.validation',
        'jquery',
        'underscore',
        'js/models/course_model',
        'js/models/pagination_model',
        'js/models/program_model',
        'js/views/course_run_view',
        'text!templates/course_details.underscore',
        'gettext',
        'js/utils/validation_config'
    ],
    function( Backbone, BackboneValidation, $, _, CourseModel, ProgramsModel,
              ProgramModel, CourseRunView, ListTpl ) {
        'use strict';

        return Backbone.View.extend({
            parentEl: '.js-course-list',

            className: 'course-details',

            events: {
                'click .js-remove-course': 'destroy',
                'click .js-select-course': 'setCourse'
            },

            tpl: _.template( ListTpl ),

            // For managing subViews
            courseRuns: [],

            initialize: function( options ) {

                this.programModel = new ProgramModel();
                this.model = new CourseModel();
                Backbone.Validation.bind( this );
                this.$parentEl = $( this.parentEl );
                this.programStatus = options.programStatus;

                // Data passed in because it is not an actual model
                if ( options.data ) {
                    this.programModel.set( options.data );
                } else {
                    this.setDefaultModel();
                }

                //this.programModel.on('change:display_name', this.update, this);
                this.render();
            },

            render: function() {
                var data = _.extend( this.programModel.toJSON(), {
                    cid: this.programModel.cid
                });

                this.$el.html( this.tpl( data ) );
                this.$parentEl.append( this.$el );
                this.postRender();
            },

            postRender: function() {
                var runs = this.programModel.get('run_modes');

                if ( runs && runs.length > 0 ) {
                    this.addCourseRuns();
                }
            },

            addCourseRuns: function() {
                // Create run views
                var runs = this.programModel.get('run_modes'),
                    $runsContainer = this.$el.find('.js-course-runs');

                _.each( runs, function( run ) {
                    var runView = new CourseRunView({
                        model: this.programModel,
                        data: run,
                        $parentEl: $runsContainer
                    });

                    this.courseRuns.push( runView );

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
                var runs = this.courseRuns;

                _.each( runs, function( run ) {
                    run.destroy();
                });
            },

            setCourse: function( event ) {
                var $form = this.$('.js-course-form'),
                    title = $form.find('.display-name').val(),
                    key = $form.find('.course-key').val();

                event.preventDefault();

                this.model.set({
                    display_name: title,
                    key: key,
                    // TODO: Update after next PR which changes this code
                    organization: {}
                });

                if ( this.model.isValid(true) ) {
                    return true;
                    // Get course runs
                    // this.programModel.fetch();
                    
                    // With the response set org 
                    // this.programModel.set({
                    //     display_name: title,
                    //     key: key,
                    //     organization: {
                    //         display_name: 'added-course-org-display-name',
                    //         key: 'added-course-org-key',
                    //     },
                    //     run_modes: [
                    //         {
                    //             course_key: 'course-v1:edX+DemoX+Demo_Course',
                    //             mode_slug: 'honor',
                    //             sku: null,
                    //             start_date: 'May 23, 2015'
                    //         }, {
                    //             course_key: 'course-v1:edX+DemoX+Demo_Course',
                    //             mode_slug: 'honor',
                    //             sku: null,
                    //             start_date: 'August 01, 2015'
                    //         }, {
                    //             course_key: 'course-v1:edX+DemoX+Demo_Course',
                    //             mode_slug: 'honor',
                    //             sku: null,
                    //             start_date: 'December 11, 2015'
                    //         }
                    //     ]
                    // });
                    //this.addCourseRuns();
                }
            },

            setDefaultModel: function() {
                this.programModel.set({
                    display_name: false,
                    programStatus: 'unpublished',
                    // TODO: Update after next PR which changes this code
                    organization: {}
                });
            }

            // TODO: Determine whether this is still needed
            // update: function() {
            //     var data = _.extend( this.programModel.toJSON(), {
            //         cid: this.programModel.cid
            //     });

            //     this.$el.html( this.tpl( data ) );
            // }
        });
    }
);
