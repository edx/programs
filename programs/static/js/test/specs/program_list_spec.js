define([
        'jquery',
        'js/models/pagination_model',
        'js/views/program_list_view'
    ],
    function( $, ProgramsModel, ProgramListView ) {
        'use strict';

        describe('ProgramListView', function() {
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
                };

            beforeEach( function() {
                // Set the DOM
                setFixtures( '<div class="js-program-admin"></div>' );

                jasmine.clock().install();

                model = new ProgramsModel();
                model.set( listData );
                model.setResults( listData.results );

                view = new ProgramListView({
                    model: model
                });
            });

            afterEach( function() {
                view.undelegateEvents();
                view.remove();

                jasmine.clock().uninstall();
            });

            it( 'should exist', function() {
                expect( view ).toBeDefined();
            });

            it( 'should render a list of 4 programs', function() {
                var $ul = view.$el.find('.program-list');

                expect( $ul.find('li').length ).toEqual( listData.count );
            });

            it( 'should render a button to create a new program if the programs list is empty', function() {
                expect( view.$el.find('.create-program-link') ).not.toBeInDOM();
                view.model.setResults( [] );
                view.render();
                expect( view.$el.find('.create-program-link') ).toBeInDOM();
            });

            it( 'should hit the API via the pagination model: error', function() {
                spyOn( $, 'ajax' ).and.callFake( function( event ) {
                    event.error( 'Error', view );
                });

                view.model.getList();

                // $.ajax should have been called
                expect($.ajax).toHaveBeenCalled();
            });

            it( 'should hit the API via the pagniation model: success', function() {
                spyOn( $, 'ajax' ).and.callFake( function( event ) {
                    event.success( listData );
                });

                view.model.getList();

                // $.ajax should have been called
                expect($.ajax).toHaveBeenCalled();
            });

            it( 'should destroy the view when the destroy function is called', function() {
                expect( view.$parentEl.html().length ).toBeGreaterThan( 0 );
                view.destroy();
                expect( view.$parentEl.html().length ).toEqual( 0 );
            });
        });
    }
);
