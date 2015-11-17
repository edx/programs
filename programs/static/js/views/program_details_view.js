define([
        'backbone',
        'backbone.validation',
        'jquery',
        'underscore',
        'js/models/course_list_model',
        'js/models/pagination_model',
        'js/views/course_details_view',
        'text!templates/program_details.underscore',
        'gettext',
        'js/utils/validation_config'
    ],
    function( Backbone, BackboneValidation, $, _, CourseListModel, ProgramsModel,
              CourseView, ListTpl ) {
        'use strict';

        return Backbone.View.extend({
            el: '.js-program-admin',

            events: {
                'blur .js-inline-edit input': 'checkEdit',
                'click .js-add-course': 'addCourse',
                'click .js-enable-edit': 'editField',
                'click .js-publish-program': 'confirmPublish'
            },

            tpl: _.template( ListTpl ),

            initialize: function() {
                Backbone.Validation.bind( this );
                this.courseList = new CourseListModel();
                this.render();
            },

            render: function() {
                this.$el.html( this.tpl( this.model.toJSON() ) );
                this.postRender();
            },

            postRender: function() {
                var courses = this.model.get('course_codes');

                _.each( courses, function( course ) {
                    var title = course.key + 'Course';

                    this[ title ] = new CourseView({
                        collection: courses,
                        data: course
                    });
                }.bind(this) );
            },

            addCourse: function() {
                return new CourseView({
                    collection: this.model.get('course_codes'),
                    courseList: this.courseList
                });
            },

            checkEdit: function( event ) {
                var $input = $(event.target),
                    $span = $input.prev('.js-model-value'),
                    $btn = $input.next('.js-enable-edit'),
                    value = $input.val(),
                    key = $input.data('field'),
                    data = {};

                data[key] = value;

                $input.addClass('is-hidden');
                $btn.removeClass('is-hidden');
                $span.removeClass('is-hidden');

                if ( this.model.get( key ) !== value ) {
                    this.model.set( data );

                    if ( this.model.isValid( true ) ) {
                        this.model.save({
                            patch: true,
                            update: data
                        });
                        $span.html( value );
                    }
                }
            },

            /**
             * Loads modal that user clicks a confirmation button
             * in to publish the course (or they can cancel out of it)
             */
            confirmPublish: function( event ) {
                event.preventDefault();

                /**
                 * TODO: add modal which will call this.publishProgram
                 * if user clicks button to confirm
                 */
                this.publishProgram();
            },

            editField: function( event ) {
                /**
                 * Making the assumption that users can only see
                 * programs that they have permission to edit
                 */
                var $btn = $( event.currentTarget ),
                    $el = $btn.prev( 'input' );

                event.preventDefault();

                $el.prev( '.js-model-value' ).addClass( 'is-hidden' );
                $el.removeClass( 'is-hidden' )
                   .addClass( 'edit' )
                   .focus();
                $btn.addClass( 'is-hidden' );
            },

            publishProgram: function() {
                this.model.set( 'status', 'active' );
                this.model.save({ patch: true });
            }
        });
    }
);
