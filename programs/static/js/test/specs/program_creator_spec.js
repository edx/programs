define([
        'jquery',
        'js/models/pagination_model',
        'js/views/program_creator_view'
    ],
    function( $, ProgramsModel, ProgramCreatorView ) {
        'use strict';

        describe('ProgramCreatorView', function () {
            var view = {},
                model = {},
                listData = {
                    count: 4,
                    next: null,
                    num_pages: 1,
                    previous: null,
                    results: [
                        {
                            category: 'xseries',
                            course_codes: [],
                            created: '2015-10-20T18:11:28.454174Z',
                            id: 2,
                            modified: '2015-10-20T18:11:28.454370Z',
                            name: 'active program',
                            organizations: [],
                            status: 'active',
                            subtitle: 'test-subtitle'
                        }, {
                            category: 'xseries',
                            course_codes: [],
                            created: '2015-10-20T18:11:28.455301Z',
                            id: 3,
                            modified: '2015-10-20T18:11:28.455466Z',
                            name: 'retired program',
                            organizations: [],
                            status: 'retired',
                            subtitle: 'test-subtitle'
                        }, {
                            category: 'xseries',
                            course_codes: [],
                            created: '2015-10-20T18:11:28.455301Z',
                            id: 4,
                            modified: '2015-10-20T18:11:28.455466Z',
                            name: 'retired program 2',
                            organizations: [],
                            status: 'retired',
                            subtitle: 'test-subtitle'
                        }, {
                            category: 'xseries',
                            course_codes: [{
                                display_name: 'test-course-display_name',
                                key: 'test-course-key',
                                organizations: {
                                    display_name: 'test-org-display_name',
                                    key: 'test-org-key'
                                },
                                run_modes: []
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
                        }
                    ]
                },
                organizations = {
                    count: 1,
                    previous: null,
                    'num_pages': 1,
                    results:[{
                        'display_name': 'test-org-display_name',
                        'key': 'test-org-key'
                    }],
                    next: null
                },
                sampleInput = {
                    organizations: 'test-org-key',
                    name: 'Test Course Name',
                    subtitle: 'Test Course Subtitle',
                    marketing_slug: 'test-management'
                },
                completeForm = function( data ) {
                    view.$el.find('#program-name').val( data.name );
                    view.$el.find('#program-subtitle').val( data.subtitle );
                    view.$el.find('#program-org').val( data.organizations );

                    if ( data.category ) {
                        view.$el.find('#program-type').val( data.category );
                    }

                    if ( data.marketing_slug ) {
                        view.$el.find('#program-marketing-slug').val( data.marketing_slug );
                    }
                },
                verifyValidation = function ( data, invalidAttr ) {
                    var errorClass = 'has-error',
                        $invalidElement = view.$el.find( '[name="' + invalidAttr + '"]' ),
                        $errorMsg = $invalidElement.siblings('.field-message'),
                        inputErrorMsg = '';

                    completeForm( data );

                    view.$el.find('.js-create-program').click();
                    inputErrorMsg = $invalidElement.data('error');

                    expect( view.model.save ).not.toHaveBeenCalled();
                    expect( $invalidElement ).toHaveClass( errorClass );
                    expect( $errorMsg ).toHaveClass( errorClass );
                    expect( inputErrorMsg ).toBeDefined();
                    expect( $errorMsg.find('.field-message-content').html() ).toEqual( inputErrorMsg );
                };

            beforeEach( function() {
                // Set the DOM
                setFixtures( '<div class="js-program-admin"></div>' );

                jasmine.clock().install();

                spyOn( ProgramsModel.prototype, 'getList' );

                model = new ProgramsModel();
                model.set( listData );
                model.setResults( listData.results );

                spyOn( ProgramCreatorView.prototype, 'saveSuccess' ).and.callThrough();
                spyOn( ProgramCreatorView.prototype, 'saveError' ).and.callThrough();

                view = new ProgramCreatorView({
                    programsModel: model
                });

                view.organizations.set( organizations );
                view.render();
            });

            afterEach( function() {
                view.destroy();

                jasmine.clock().uninstall();
            });

            it( 'should exist', function () {
                expect( view ).toBeDefined();
            });

            it ( 'should get the form data', function() {
                var formData = {};

                completeForm( sampleInput );
                formData = view.getData();

                expect( formData.name ).toEqual( sampleInput.name );
                expect( formData.subtitle ).toEqual( sampleInput.subtitle );
                expect( formData.organizations[0].key ).toEqual( sampleInput.organizations );
            });

            it( 'should submit the form when the user clicks submit', function() {
                completeForm( sampleInput );

                spyOn( $, 'ajax' ).and.callFake( function( event ) {
                    event.success();
                });

                view.$el.find('.js-create-program').click();

                expect( $.ajax ).toHaveBeenCalled();
                expect( view.saveSuccess ).toHaveBeenCalled();
                expect( view.saveError ).not.toHaveBeenCalled();
                expect( view.programsModel.getList ).toHaveBeenCalled();
            });

            it( 'should run the saveError when model save failures occur', function() {
                spyOn( $, 'ajax' ).and.callFake( function( event ) {
                    event.error();
                });

                // Fill out the form with valid data so that form model validation doesn't
                // prevent the model from being saved.
                completeForm( sampleInput );
                view.$el.find('.js-create-program').click();

                expect( $.ajax ).toHaveBeenCalled();
                expect( view.saveSuccess ).not.toHaveBeenCalled();
                expect( view.saveError ).toHaveBeenCalled();
            });

            it( 'should set the model when valid form data is submitted', function() {
                completeForm( sampleInput );

                spyOn( $, 'ajax' ).and.callFake( function( event ) {
                    event.success();
                });

                view.$el.find('.js-create-program').click();

                expect( view.model.get('name') ).toEqual( sampleInput.name );
                expect( view.model.get('subtitle') ).toEqual( sampleInput.subtitle );
                expect( view.model.get('organizations')[0].key ).toEqual( sampleInput.organizations );
                expect( view.model.get('marketing_slug') ).toEqual( sampleInput.marketing_slug );
            });

            it( 'should not set the model when an invalid program name is submitted', function() {
                var invalidInput = $.extend({}, sampleInput);

                spyOn( view.model, 'save' );

                // No name provided.
                invalidInput.name = '';
                verifyValidation( invalidInput, 'name' );

                // Name is too long.
                invalidInput.name = 'x'.repeat(100);
                verifyValidation( invalidInput, 'name' );
            });

            it( 'should not set the model when an invalid program subtitle is submitted', function() {
                var invalidInput = $.extend({}, sampleInput);

                spyOn( view.model, 'save' );

                // Subtitle is too long.
                invalidInput.subtitle = 'x'.repeat(300);
                verifyValidation( invalidInput, 'subtitle' );
            });

            it( 'should not set the model when an invalid category is submitted', function() {
                var invalidInput = $.extend({}, sampleInput);

                spyOn( view.model, 'save' );

                // Category other than 'xseries' selected.
                invalidInput.category = 'yseries';
                verifyValidation( invalidInput, 'category' );
            });

            it( 'should not set the model when an invalid organization key is submitted', function() {
                var invalidInput = $.extend({}, sampleInput);

                spyOn( view.model, 'save' );

                // No organization selected.
                invalidInput.organizations = 'false';
                verifyValidation( invalidInput, 'organizations' );
            });

            it( 'should not set the model when an invalid marketing slug is submitted', function() {
                var invalidInput = $.extend({}, sampleInput);

                spyOn( view.model, 'save' );

                // Marketing slug is too long.
                invalidInput.marketing_slug = 'x'.repeat(256);
                verifyValidation( invalidInput, 'marketing_slug' );
            });

            it( 'should abort the view when the cancel button is clicked', function() {
                completeForm( sampleInput );
                expect( view.$parentEl.html().length ).toBeGreaterThan( 0 );
                view.$el.find('.js-abort-view').click();
                expect( view.$parentEl.html().length ).toEqual( 0 );
            });
        });
    }
);
