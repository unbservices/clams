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
# some easier-on-the-eyes syntax, we're still not seeing a lot of win.
#
# One of the major benefits of Clams is that you don't have to start with the
# root command and build up (the way you have to in argparse).  To show this,
# let's build a sub-command that provides a, very limited, interface to git.


# unb git
# -------

# Let's get some imports out of the way first.  Since we're not going to
# actually implement any of git, we need to have a method of calling the
# system's git commands to perform the work for us.  Subprocess is a great way
# to do that.

import subprocess


# First we will create our `git` sub-command.  If you're paying attention,
# you'll notice that we have not mentioned the root command at all (but we'll
# see what this means a bit later).

git = Command('git')


# Let's start by implementing a very simple version of `git commit`.
#
# One of the standout features of Clams is that the argparse interface is
# exposed directly, for... you know... parsing args.
#
# The `arg` decorator has exactly the same interface as
# `argparse.ArgumentParser().add_argument`.  In fact, in its most basic form,
# all the `arg` decorator does is pass it's arguments directly to
# `add_argument` as `some_parser.add_argument(*args, **kwargs)`.

@git.register('commit')
@arg('-m', '--message')
@arg('-a', '--all', action='store_true', default=False)
def handler(all, message):
    git_command = ['git', 'commit']
    if all:
        git_command.append('-a')
    if message:
        git_command.append('-m')
        git_command.append(message)
    return subprocess.call(git_command)


# Finally, we'll register our `git` sub-command with our `unb` root command.

unb.add_command(git)


# And that's it!  We can now run commands like:
#
#     unb git add .
#     unb git commit -m "My awesome commit message"
#     unb git remote add my_remote_name https://.../myrepo.git
#
# Well... not quite yet.
#
# Until this point, all of the `add_command`s and `register`s we've been
# calling haven't actually built any argparse parsers!
#
# Instead, we've just been storing all the information to build these parsers
# in simple lists, tuples and dicts within each Command instance.  To build the
# actual parsers (essential if we're going to actually *use* this), we need to
# call the root command's `init` function (with no arguments).
#
# This will create the main argparse entrypoint (`argparse.ArgumentParser`) and
# recursively build all of its sub-commands by calling their `init` methods
# with itself as the parent/`command` argument.  Each sub-command will,
# in-turn, call its own `init` method with itself as the parent/`command`
# argument.  This allows us to create arbitrarily deep sub-commands (until we
# hit Python's maximum recursion depth, anyway).

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
