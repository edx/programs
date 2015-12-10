define([
        'jquery',
        'js/models/program_model',
        'js/views/program_details_view',
        'js/utils/constants'
    ],
    function( $, ProgramModel, ProgramDetailsView, constants ) {
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
                    marketing_slug: 'test-program-slug',
                    modified: '2015-10-20T18:11:46.854735Z',
                    name: 'test-program-5',
                    organizations: [{
                        display_name: 'test-org-display_name',
                        key: 'test-org-key'
                    }],
                    status: 'unpublished',
                    subtitle: 'test-subtitle'
                },
                testTimeoutInterval = 100,
                errorClass = 'has-error',
                completeCourseForm,
                editField,
                keyPress,
                openPublishModal,
                testHidingButtonsAfterPublish,
                testInvalidUpdate,
                testUnchangedFieldBlur,
                testUpdatedFieldBlur;

            completeCourseForm = function() {
                var $form = view.$('.js-course-form');

                $form.find('.course-key').val('123');
                $form.find('.display-name').val('test course 1');
            };

            editField = function( el, str ) {
                var $input = view.$el.find( el ),
                    $btn = $input.next( '.js-enable-edit' );

                expect( document.activeElement ).not.toEqual( $input[0] );
                expect( $input ).not.toHaveClass( 'edit' );
                expect( $input ).toHaveClass( 'is-hidden' );

                $btn.click();

                $input.val( str );

                // Enable editing
                expect( $input ).not.toHaveClass( 'is-hidden' );
                expect( $input ).toHaveClass( 'edit' );
            };

            keyPress = function( $el, key ) {
                $el.trigger({
                    type: 'keydown',
                    keyCode: key,
                    which: key,
                    charCode: key
                });
            };

            openPublishModal = function() {
                var $publishBtn = view.$el.find('.js-publish-program'),
                    defaultStatus = programData.status,
                    publishedStatus = 'active';

                expect( view.modalView ).not.toBeDefined();
                expect( view.model.get( 'status' ) ).toEqual( defaultStatus );
                expect( view.model.get( 'status' ) ).not.toEqual( publishedStatus );

                $publishBtn.click();
            };

            testUnchangedFieldBlur = function( el ) {
                var $input = view.$el.find( el ),
                    $btn = view.$el.find( '.js-add-course' ),
                    title = $input.val(),
                    update = title;

                editField( el, update );
                $btn.focus();
                $input.blur();

                expect( title ).toEqual( update );
                expect( view.model.save ).not.toHaveBeenCalled();
            };

            testUpdatedFieldBlur = function( el, update ) {
                var $input = view.$el.find( el ),
                    $btn = view.$el.find( '.js-add-course' );

                expect( $input.val() ).not.toEqual( update );

                editField( el, update );

                $btn.focus();
                $input.blur();

                expect( $input.val() ).toEqual( update );
                expect( view.model.save ).toHaveBeenCalled();
            };

            testHidingButtonsAfterPublish = function( el ) {
                expect( view.$el.find( el ).length ).toBeGreaterThan( 0 );
                view.model.set({ status: 'active' });
                view.render();
                expect( view.$el.find( el ).length ).toEqual( 0 );
            };

            testInvalidUpdate = function( el, update ) {
                var $input = view.$el.find( el ),
                    $btn = view.$el.find( '.js-add-course' );

                editField( el, update );

                $btn.focus();
                $input.blur();

                expect( $input ).toHaveClass( errorClass );
                expect( view.model.save ).not.toHaveBeenCalled();
            };

            beforeEach( function() {
                // Set the DOM
                setFixtures( '<div class="js-program-admin"></div>' );

                jasmine.clock().install();

                spyOn( ProgramModel.prototype, 'set' ).and.callThrough();
                spyOn( ProgramModel.prototype, 'save' );

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

            describe( 'View data', function() {
                it( 'should exist', function () {
                    expect( view ).toBeDefined();
                });

                it( 'should render all of the run_modes from the model', function () {
                   var $runs = view.$el.find('.js-course-runs'),
                       domLength = $runs.find('.js-remove-run').length,
                       objLength = programData.course_codes[0].run_modes.length;

                    expect( domLength ).toEqual( objLength );
                });
            });

            describe( 'Delete data', function() {
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

                it( 'should not show the delete course button if program status is not unpublished', function() {
                    testHidingButtonsAfterPublish('.js-remove-course');
                });

                it( 'should not show the add course button if program status is not unpublished', function() {
                    testHidingButtonsAfterPublish('.js-add-course');
                });

                it( 'should not show the delete run button if program status is not unpublished', function() {
                    testHidingButtonsAfterPublish('.js-remove-run');
                });
            });

            describe( 'Add data', function() {
                it( 'should add a new course details view on click of the add course button', function() {
                    var $btn = view.$el.find('.js-add-course').first();

                    expect( view.$('.js-course-form').length ).toEqual( 0 );
                    $btn.click();
                    expect( view.$('.js-course-form').length ).toEqual( 1 );
                });

                it( 'should add a course when the form is submitted', function() {
                    var $addCourseBtn = view.$el.find('.js-add-course').first(),
                        $form,
                        $submitBtn;

                    expect( view.$el.find('.course-details').length ).toEqual( 1 );
                    $addCourseBtn.click();
                    $form = view.$('.js-course-form');
                    $submitBtn = $form.find('.js-select-course');
                    completeCourseForm();
                    $submitBtn.click();
                    expect( $form.find('.field-message.has-error').length ).toEqual( 0 );
                });

                it( 'should not submit the course form when it is incomplete', function() {
                    var $addCourseBtn = view.$el.find('.js-add-course').first(),
                        $form,
                        $submitBtn;

                    expect( view.$el.find('.course-details').length ).toEqual( 1 );
                    $addCourseBtn.click();
                    $form = view.$('.js-course-form');
                    expect( $form.find('.field-message.has-error').length ).toEqual( 0 );
                    $submitBtn = $form.find('.js-select-course');
                    $submitBtn.click();
                    expect( $form.find('.field-message.has-error').length ).toEqual( 2 );
                });
            });

            describe( 'Edit data', function() {
                it( 'should enable a user to edit the name, subtitle and marketing slug fields', function() {
                    editField( '.program-name', 'name' );
                    editField( '.program-subtitle', 'subtitle' );
                    editField( '.program-marketing-slug', 'marketing-slug' );
                });

                it( 'should not send an API call if a user does not change the value of an editable field', function() {
                    testUnchangedFieldBlur( '.program-name' );
                    testUnchangedFieldBlur( '.program-subtitle' );
                    testUnchangedFieldBlur( '.program-marketing-slug' );
                });

                it( 'should send an API call if a user changes the value of an editable field', function() {
                    testUpdatedFieldBlur( '.program-name',  'new-title' );
                    testUpdatedFieldBlur( '.program-subtitle',  'new-subtitle' );
                    testUpdatedFieldBlur( '.program-marketing-slug',  'new-marketing-slug' );
                });

                it( 'should show error messaging if the updated required field is empty', function() {
                    testInvalidUpdate( '.program-name',  '' );
                });

                it( 'should show error messaging if the updated field value is too long', function() {
                    var chars65 = 'x'.repeat(65),
                        chars256 = 'x'.repeat(256);

                    testInvalidUpdate( '.program-name',  chars65 );
                    testInvalidUpdate( '.program-subtitle',  chars256 );
                    testInvalidUpdate( '.program-marketing-slug',  chars256 );
                });

                it( 'should create a POST config object by default', function() {
                    var config = view.model.getConfig();

                    expect( config.type ).toEqual( 'POST' );
                    expect( config.contentType ).toEqual( 'application/json' );
                    expect( config.data ).not.toBeDefined();
                });

                it( 'should create a PATCH config object when passed in object sets patch as true', function() {
                    var data = { name: 'patched name' },
                        config = view.model.getConfig({
                            patch: true,
                            update: data
                        });

                    expect( config.type ).toEqual( 'PATCH' );
                    expect( config.contentType ).toEqual( 'application/merge-patch+json' );
                    expect( config.data ).toBeDefined();
                    expect( config.data ).toEqual( JSON.stringify( data ) );
                });
            });

            describe( 'Publish a Program', function() {
                it( 'should open the publish modal when the publish button is clicked', function() {
                    openPublishModal();
                    expect( view.modalView ).toBeDefined();
                });

                it( 'should publish a program when the publish confirm button is clicked', function() {
                    var defaultStatus = programData.status,
                        publishedStatus = 'active';

                    openPublishModal();
                    expect( view.modalView ).toBeDefined();

                    view.$el.find('.js-confirm').click();

                    // Model should be set and save called
                    expect( view.model.set ).toHaveBeenCalled();
                    expect( view.model.get( 'status' ) ).not.toEqual( defaultStatus );
                    expect( view.model.get( 'status' ) ).toEqual( publishedStatus );
                    expect( view.model.save ).toHaveBeenCalled();

                    // Publish button should be removed once API has completed its call
                    expect( view.$el.find('.js-publish-program').length ).toEqual( 1 );
                    view.model.trigger( 'sync' );
                    expect( view.$el.find('.js-publish-program').length ).toEqual( 0 );
                });

                it( 'should show a validation error when publish button pressed if validation fails', function() {
                    var $input = view.$el.find( '#program-marketing-slug' );

                    view.model.set('marketing_slug', '');
                    openPublishModal();
                    expect( view.modalView ).not.toBeDefined();
                    expect( $input ).toHaveClass( errorClass );
                });

                it( 'should destroy the publish modal when the cancel button is clicked', function() {
                    openPublishModal();
                    expect( view.modalView ).toBeDefined();

                    // Close the modal
                    view.$el.find('.js-cancel').click();

                    // Expect the modal DOM elements to not be there anymore
                    expect( view.$el.find('.js-cancel').length ).toEqual( 0 );
                    expect( view.modalView.$parentEl.html().length ).toEqual( 0 );
                });

                it( 'should destroy the publish modal when the esc key is pressed', function() {
                    openPublishModal();
                    expect( view.modalView ).toBeDefined();

                    // Close the modal
                    keyPress( view.modalView.$el, constants.keyCodes.esc );

                    // Expect the modal DOM elements to not be there anymore
                    expect( view.$el.find('.js-cancel').length ).toEqual( 0 );
                    expect( view.modalView.$parentEl.html().length ).toEqual( 0 );
                });
            });
        });
    }
);
