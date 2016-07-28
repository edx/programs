Software Prerequisites
======================

- Clone of `edx/programs <https://github.com/edx/programs>`_

- Python 2.7.x (and pip)

=======


Virtualenvwrapper
-----------------

For some general background and basic virtualenvwrapper usage, please consult the
Hitchhiker's guide to Python's `section on virtualenv`_.

 .. _section on virtualenv: http://docs.Python-guide.org/en/latest/dev/virtualenvs/#virtualenvwrapper

1. On your local machine, if you haven't already, install pip.

.. code-block:: bash

    $ sudo easy_install pip

2. Once pip is installed, you will need to install virtualenvwrapper.

.. code-block:: bash

    $ sudo pip install virtualenvwrapper

3. If (like me) you get an error while trying to uninstall the 'six' package, modify the command above to ignore six.

.. code-block:: bash

    $ sudo pip install virtualenvwrapper --ignore-installed six

4. Once installed, follow the instructions on setting up `virtualenvwrapper`_

.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.io/en/latest/

5. Create a new virtualenv for programs.

.. code-block:: bash

    $ mkvirtualenv programs

6. You should now see a terminal that has a prompt that looks something like the prompt below.  This signifies that
your current working directory is the programs directory, and you are currently in the Python virtual environment
called programs.

.. code-block:: bash

    (programs) MikesMacBook:programs mike$

Continuing Installation
-----------------------

7. Confirm that you have the LMS running in devstack.  If you don't, please consult the `Running Devstack`_ wiki document for instructions.

.. _Running Devstack: https://openedx.atlassian.net/wiki/display/OpenOPS/Running+Devstack

8. Refer to the programs `Getting Started`_ document for setting up the programs service now that the prereqs
(node, pip, virtualenv) are met.

.. _Getting Started: getting_started.html
