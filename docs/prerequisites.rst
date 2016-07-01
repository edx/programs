Software Prerequisites
======================

- Python 2.7.x (and pip)
.. (Empty comment for new line...)
- Clone of `edx/programs`_ (github repository)
.. _edx/programs: https://github.com/edx/programs

- `Node.js 4.4.x`_ (and npm) (download or use nvm - explained below)
.. _Node.js 4.4.x: https://nodejs.org/download/release/v4.4.7/


nvm (Optional)
--------------

One easy way to manage the different node versions you may have installed on your machine is to use `nvm`_.

.. _nvm: https://github.com/creationix/nvm

With nvm, you can easily switch from one node version to another, and even declare the version of node that
a project needs to work with in a hidden file that is read in by nvm in the working directory. If using nvm,
simply change directories to the programs directory from the github checkout and use this command:

.. code-block:: bash

    $ nvm use

If you already have Node.js version 4.4.x installed, nvm will switch to using it.  If not, use this command to install
(and switch to) it:

.. code-block:: bash

    $ nvm install

Virtualenvwrapper/pip Installation
----------------------------------

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

.. _Getting Started: getting_started.rst