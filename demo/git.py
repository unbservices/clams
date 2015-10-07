"""
Clams Git
=========

This is the executable source-code version of git.rst.

"""

from clams import arg, Command

# Let's get some imports out of the way first.  Since we're not going to actually
# implement any of git, we need to have a method of calling the system's git
# commands to perform the work for us.  Subprocess is a great way to do that.

import subprocess


# First we will create our `git` subcommand.  If you're paying attention,
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


# TODO(nick): Finish converting this!
# ===================================

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
# recursively build all of its subcommands by calling their `init` methods
# with itself as the parent/`command` argument.  Each subcommand will,
# in-turn, call its own `init` method with itself as the parent/`command`
# argument.  This allows us to create arbitrarily deep subcommands (until we
# hit Python's maximum recursion depth, anyway).

git.init()


if __name__ == '__main__':

    # Just like argparse, we call the root command's `parse_args` method to
    # retrieve the arguments from `sys.argv` and parse them.
    #
    # When a subcommand is found, the remainder of the arguments will be
    # passed to its handler function, which will perform its action and
    # (optionally) return some value.  `parse_args` does return this value, but
    # it isn't beneficial to us, so we'll just ignore it.

    git.parse_args()
