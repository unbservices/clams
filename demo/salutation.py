#!/usr/bin/env python
"""
Simple Salutations Example
==========================

This is the first example in the /README.md file in an executable file.

Usage:

    $ cd demo

    $ ./salutation.py hello
    Hello Nick

    $ ./salutation.py hello Jason
    Hello Jason

    $ ./salutation.py goodbye "my friend."
    Goodbye my friend.

"""
from __future__ import print_function
from __future__ import unicode_literals

from clams import arg, Command


salutation = Command('salutation')


@salutation.register('hello')
@arg('name', nargs='?')  # <== same interface as argparse's `add_argument`
def handler(name):
    print('Hello %s' % (name or 'Nick'))


@salutation.register('goodbye')
@arg('name', nargs='?')
def handler(name):
    print('Goodbye %s' % (name or 'Nick'))


if __name__ == '__main__':
    salutation.init()
    salutation.parse_args()
