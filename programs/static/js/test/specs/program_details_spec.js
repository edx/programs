define([
        'js/models/program_model',
        'js/views/program_details_view'
    ],
    function( ProgramModel, ProgramDetailsView ) {
        'use strict';

        describe('ProgramDetailsView', function () {
            var view = {},
                model = {},
                programData = {
                    category: 'xseries',
                    course_codes: [{
                        display_name: 'test-course-display_name',
                        key: 'test-course-key',
                        organization: {
                            display_name: 'test-org-display_name',
                            key: 'test-org-key'
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
                    }],
                    created: '2015-10-20T18:11:46.854451Z',
                    id: 5,
                    modified: '2015-10-20T18:11:46.854735Z',
                    name: 'test-program-5',
                    organizations: [{
                        display_name: 'test-org-display_name',
                        key: 'test-org-key'
                    }],
                    status: 'unpublished',
                    subtitle: 'test-subtitle'
                },
                testTimeoutInterval = 100;

            beforeEach( function() {
                // Set the DOM
                setFixtures( '<div class="js-program-admin"></div>' );

                jasmine.clock().install();

                model = new ProgramModel();
                model.set( programData );

                view = new ProgramDetailsView({
                    model: model
                });
            });

            afterEach( function() {
                view.undelegateEvents();
                view.remove();

                jasmine.clock().uninstall();
            });

            it( 'should exist', function () {
                expect( view ).toBeDefined();
            });

            it( 'should render all of the run_modes from the model', function () {
               var $runs = view.$el.find('.js-course-runs');

                expect( $runs.find('.js-remove-run').length ).toEqual( programData.course_codes[0].run_modes.length );
            });

            it( 'should remove a course when the delete button is clicked', function() {
                var $el = view.$el.find('.js-course-list'),
                    $removeRunBtn = $el.find('.js-remove-course').first(),
                    count = programData.course_codes.length;

                expect( $el.find('.js-remove-course').length ).toEqual( count );
                $removeRunBtn.click();

                setTimeout( function() {
                    expect( $el.find('.js-remove-course').length ).toEqual( count - 1 );
                }, testTimeoutInterval );

                jasmine.clock().tick( testTimeoutInterval + 1 );
            });

            it( 'should remove a course run when the delete button is clicked', function() {
                var $runs = view.$el.find('.js-course-runs'),
                    $removeRunBtn = $runs.find('.js-remove-run').first(),
                    count = programData.course_codes[0].run_modes.length;

                expect( $runs.find('.js-remove-run').length ).toEqual( count );
                $removeRunBtn.click();

                setTimeout( function() {
                    expect( $runs.find('.js-remove-run').length ).toEqual( count - 1 );
                }, testTimeoutInterval );

                jasmine.clock().tick( testTimeoutInterval + 1 );
            });

            it( 'should add a new course details view on click of the add course button', function() {
                var $btn = view.$el.find('.js-add-course').first();

                expect( view.$el.find('.js-course-select').length ).toEqual( 0 );
                $btn.click();

                setTimeout( function() {
                    var $select = view.$el.find('.js-course-select');
                    expect( $select.length ).toEqual( 1 );
                }, testTimeoutInterval );

                jasmine.clock().tick( testTimeoutInterval + 1 );
            });

            it( 'should set course details on change of the course select', function() {
                var $btn = view.$el.find('.js-add-course').first();

                expect( view.$el.find('.course-details').length ).toEqual( 1 );
                $btn.click();

                setTimeout( function() {
                    view.$el.find('.js-course-select').val('002').trigger('change');
                }, testTimeoutInterval );

                setTimeout( function() {
                    expect( view.$el.find('.course-details').length ).toEqual( 2 );
                }, testTimeoutInterval * 2 );

                jasmine.clock().tick( testTimeoutInterval + 1 );
                jasmine.clock().tick( ( testTimeoutInterval * 2 ) + 1 );
            });
        });
    }
);
