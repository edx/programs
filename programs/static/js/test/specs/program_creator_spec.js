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
                                organization: {
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
                    organization: 'test-org-key',
                    name: 'Test Course Name',
                    subtitle: 'Test Course Subtitle'
                },
                completeForm = function( data ) {
                    view.$el.find('#program-name').val( data.name );
                    view.$el.find('#program-subtitle').val( data.subtitle );
                    view.$el.find('#program-org').val( data.organization );
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
                expect( formData.organization[0].key ).toEqual( sampleInput.organization );
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

                view.$el.find('.js-create-program').click();

                expect( $.ajax ).toHaveBeenCalled();
                expect( view.saveSuccess ).not.toHaveBeenCalled();
                expect( view.saveError ).toHaveBeenCalled();
            });

            it( 'should set the model with form data when submitted', function() {
                completeForm( sampleInput );

                spyOn( $, 'ajax' ).and.callFake( function( event ) {
                    event.success();
                });

                view.$el.find('.js-create-program').click();

                expect( view.model.get('name') ).toEqual( sampleInput.name );
                expect( view.model.get('subtitle') ).toEqual( sampleInput.subtitle );
                expect( view.model.get('organization')[0].key ).toEqual( sampleInput.organization );
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
