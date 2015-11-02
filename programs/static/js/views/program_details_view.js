define([
        'backbone',
        'jquery',
        'underscore',
        'js/models/course_list_model',
        'js/models/pagination_model',
        'js/views/course_details_view',
        'text!templates/program_details.underscore'
    ],
    function( Backbone, $, _, CourseListModel, ProgramsModel,
              CourseView, ListTpl ) {
        'use strict';

        return Backbone.View.extend({
            el: '.js-program-admin',

            events: {
                'click .js-add-course': 'addCourse'
            },

            tpl: _.template( ListTpl ),

            initialize: function() {
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
            }
        });
    }
);
