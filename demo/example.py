#!/usr/bin/env python
"""
Clams Examples
==============

Just some simple examples, done in a bit of a literate-programming style.

"""

from clams import Command, arg, command, register, register_command


# unb
# ===
#
# Create the root command.  For the purposes of this demo, we'll call the
# command `unb`.

unb = Command('unb')


# unb echo[n]
# -----------
#
# There's lots of ways to create sub-commands and register them with the
# parent.  We'll start with the most manual, and build up from there.


# Option 1: Manually build and connect everything

echo1 = Command('echo1')
echo1.add_arg('foo')

def _echo1(foo):
    print foo

echo1.add_handler(_echo1)

unb.add_command(echo1)


# Option 2: Use the `command` and `arg` decorators.
#
# NOTE: If you use the `arg` decorator, you must use one of the `command`
# decorators (`command`, `register_command`,
# `command_instance.register_command`, or `command_instance.register` with
# a name argument.

@command('echo2')
@arg('foo')
def echo2(foo):
    print foo

unb.add_command(echo2)


# Option 3: Use the `register` decorator.
#
# At this point we no longer need to use a meaningful name for our handler
# function, since all the actions we need to use it for are handled by the
# decorators at definition.

@register(unb)
@command('echo3')
@arg('foo')
def handler(foo):
    print foo


# Option 4: We can (arguably) make this a little cleaner by using the
# `register_command` decorator present on our parent command.

@unb.register()
@command('echo4')
@arg('foo')
def handler(foo):
    print foo


# Option 5: We can combine `register` and `command` by using the
# `register_command` decorator.

@register_command(unb, 'echo5')
@arg('foo')
def handler(foo):
    print foo


# Option 6: Slightly less arguably we can make this cleaner by using the
# `register_command` decorator present on our parent command.

@unb.register_command('echo6')
@arg('foo')
def handler(foo):
    print foo


# Option 7: Finally we can go back to the `register` decorator on the parent
# command and pass it the optional `name` argument, which will make it behave
# just like `register_command` on the parent.

@unb.register('echo7')
@arg('foo')
def handler(foo):
    print foo


# This is all a bit neater than the standard argparse interface, but other than
# some easier-on-the-eyes syntax, we're still not seeing a lot of
#
# Check out /demo/git for a more advanced example.


unb.init()


if __name__ == '__main__':

    # Just like argparse, we call the root command's `parse_args` method to
    # retrieve the arguments from `sys.argv` and parse them.
    #
    # When a sub-command is found, the remainder of the arguments will be
    # passed to its handler function, which will perform its action and
    # (optionally) return some value.  `parse_args` does return this value, but
    # it isn't beneficial to us, so we'll just ignore it.

    unb.parse_args()
