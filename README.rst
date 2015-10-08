Clams
=====

Create simple, nested, command-line interfaces with Clams (Command Line
Applications Made Simple).


Installation
------------

.. code-block:: console

   pip install clams


Example
-------

A simple example with ``hello`` and ``goodbye`` subcommands.  This can be
found at `/demo/salutation.py </demo/salutation.py>`_.


.. code-block:: python

    from clams import arg, Command


    salutation = Command('salutation')


    @salutation.register('hello')
    @arg('name', nargs='?')  # same interface as argparse's ``add_argument``
    def handler(name):
        print 'Hello %s' % (name or 'Nick')


    @salutation.register('goodbye')
    @arg('name', nargs='?')
    def handler(name):
        print 'Goodbye %s' % (name or 'Nick')


    if __name__ == '__main__':
        salutation.init()
        salutation.parse_args()


Usage:

.. code-block:: console

   $ cd demo

   $ ./salutation.py hello
   Hello Nick


.. code-block:: console

   $ ./salutation.py hello Jason
   Hello Jason

   $ ./salutation.py goodbye "my friend."
   Goodbye my friend.





Documentation
-------------

Clams documentation is `available on ReadTheDocs
<http://clams.readthedocs.org/en/latest/>`_ and can be found locally in the
`/docs </docs>`_ directory.


Issue Reporting and Contact Information
---------------------------------------

If you have any problems with this software, please take a moment to report
them at https://github.com/unbservices/clams or by email to nick@unb.services.

If you are a security researcher or believe you have found a security
vulnerability in this software, please contact us by email at
nick@unb.services.


Contributing
------------

Contributions are always welcome, whether it's reporting a bug or sending a
pull request.  If you want to help, but don't know where to start, email me at
nick@unb.services and I'll try to point you in the right direction.


Copyright and License Information
---------------------------------

Copyright (c) 2015 Nick Zarczynski

This project is licensed under the MIT license.  Please see the LICENSE file
for more information.
