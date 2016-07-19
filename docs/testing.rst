Testing
=======

To run the unit tests and get a code coverage report:

.. code-block:: bash

    $ make test

To run a single test, remove the compiled python files picked up by the test launcher and provide the path to the
single test:

.. code-block:: bash

    $ make clean
    $ ./manage.py test programs/path/to/your/python_test.py --settings=programs.settings.test

The command below runs the Python tests and code quality validation—Pylint and PEP8.

.. code-block:: bash

    $ make validate

Code quality validation can be run independently with:

.. code-block:: bash

    $ make quality

Acceptance Testing
------------------

Acceptance tests for this project are intended for use with Studio, where the Programs admin tool is used.


Definitions
***********

Definitions of commonly used terms:

* LMS: The edX Learning Management System. Course content is found here.
* CMS: The Studio system that facilitate the course content creation and management and program management.
* Programs: The application that stores and manages the data set which group a set of courses defined by studio user


Environment Variables
*********************

Our acceptance tests rely on configuration which are specified using environment variables below.

======================== ========================================================================= ========= ============================================================
Variable                 Description                                                               Required? Default Value
======================== ========================================================================= ========= ============================================================
STUDIO_URL_ROOT          URL root for the CMS platform Service                                     Yes       N/A
LMS_URL_ROOT             URL root for the LMS platform Service                                     Yes       N/A
PROGRAMS_URL_ROOT        URL root for the Programs Service                                         Yes       N/A
STUDIO_EMAIL             The email of the user to log into CMS                                     NO        N/A
STUDIO_PASSWORD          The password of the user to log into CMS                                  NO        N/A
LMS_AUTO_AUTH            The flag for whether to use auto auth capability on LMS                   No        True
ALLOW_DELETE_ALL_PROGRAM The flag for whether allow the acceptance test to delete all programs     No        False
PROGRAM_ORGANIZATION     The organization to choose when creating the new program                  No        'edx'
BASIC_AUTH_USERNAME      Username used to bypass HTTP basic auth on the LMS                        No        N/A
BASIC_AUTH_PASSWORD      Password used to bypass HTTP basic auth on the LMS                        No        N/A
======================== ========================================================================= ========= ============================================================

Note:
If STUDIO_EMAIL and STUDIO_PASSWORD are provided, they will be used for all tests. This means that the tests will not use auto-auth. If LMS_AUTO_AUTH is set to "False" and STUDIO_EMAIL and STUDIO_PASSWORD are not specified, the tests will fail. This is because the tests needs user credentials to access Studio.

Running Acceptance Tests
************************

Run all acceptance tests by executing ``make accept``. To run a specific test, execute::

    $ nosetests -v <path/to/the/test/module>

As discussed above, the acceptance tests rely on configuration which can be specified using environment variables. For example, when running the acceptance tests against local instances of LMS, CMS and Programs, you might run:

    $ PROGRAMS_URL_ROOT="http://localhost:8004" LMS_URL_ROOT="http://localhost:8000" STUDIO_URL_ROOT="http://localhost:8001" LMS_AUTO_AUTH="true" ALLOW_DELETE_ALL_PROGRAM="true" make accept

When running against a production-like staging environment, you might run::

    $ PROGRAMS_URL_ROOT="https://programs.stage.edx.org" LMS_URL_ROOT="https://courses.stage.edx.org" STUDIO_URL_ROOT="http://studio.stage.edx.org" LMS_AUTO_AUTH="true" make accept
