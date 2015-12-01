define([
        'backbone',
        'backbone.validation',
        'jquery',
        'underscore',
        'js/models/course_list_model',
        'js/models/pagination_model',
        'js/views/confirm_modal_view',
        'js/views/course_details_view',
        'text!templates/program_details.underscore',
        'gettext',
        'js/utils/validation_config'
    ],
    function( Backbone, BackboneValidation, $, _, CourseListModel, ProgramsModel,
              ModalView, CourseView, ListTpl ) {
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
                var courses = this.model.get( 'course_codes' );

                _.each( courses, function( course ) {
                    var title = course.key + 'Course',
                        data = $.extend( course, { programStatus: this.model.get( 'status' ) });

                    this[ title ] = new CourseView({
                        collection: courses,
                        data: data
                    });
                }.bind(this) );

                // Stop listening to the model sync set when publishing
                this.model.off( 'sync' );
            },

            addCourse: function() {
                return new CourseView({
                    collection: this.model.get('course_codes'),
                    courseList: this.courseList
                });
            },

            checkEdit: function( event ) {
                var $input = $(event.target),
                    $span = $input.prevAll('.js-model-value'),
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
                        this.model.patch( data );
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
                 * Update validation to make marketing slug required
                 * Note that because this validation is not required for
                 * the program creation form and is only happening here
                 * it makes sense to have the validation at the view level
                 */
                if ( this.model.isValid( true ) && this.validateMarketingSlug() ) {
                    this.modalView = new ModalView({
                        model: this.model,
                        callback: _.bind( this.publishProgram, this ),
                        content: this.getModalContent(),
                        parentEl: '.js-publish-modal',
                        parentView: this
                    });
                }
            },

            editField: function( event ) {
                /**
                 * Making the assumption that users can only see
                 * programs that they have permission to edit
                 */
                var $btn = $( event.currentTarget ),
                    $el = $btn.prev( 'input' );

                event.preventDefault();

                $el.prevAll( '.js-model-value' ).addClass( 'is-hidden' );
                $el.removeClass( 'is-hidden' )
                   .addClass( 'edit' )
                   .focus();
                $btn.addClass( 'is-hidden' );
            },

            getModalContent: function() {
                /* jshint maxlen: 300 */
                return {
                    name: gettext('confirm'),
                    title: gettext('Publish this program?'),
                    body: gettext('After you publish this program, you cannot add or remove course codes or remove course runs.'),
                    cta: {
                        cancel: gettext('Cancel'),
                        confirm: gettext('Publish')
                    }
                };
            },

            publishProgram: function() {
                var data = {
                    status: 'active'
                };

                this.model.set( data, { silent: true } );
                this.model.on( 'sync', this.render, this );
                this.model.patch( data );
            },

            validateMarketingSlug: function() {
                var isValid = false,
                    $input = {},
                    $message = {};

                if ( this.model.get( 'marketing_slug' ).length > 0 ) {
                    isValid = true;
                } else {
                    $input = this.$el.find( '#program-marketing-slug' );
                    $message = $input.siblings( '.field-message' );

                    // Update DOM
                    $input.addClass( 'has-error' );
                    $message.addClass( 'has-error' );
                    $message.find( '.field-message-content' )
                        .html( gettext( 'Marketing Slug is required.') );
                }

                return isValid;
            }
        });
    }
);
