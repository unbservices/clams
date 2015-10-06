Clams Git
=========

Let's take a look at how Clams can help you build a moderately complex
command line interface. We're going to build a "git porcelain", otherwise
known as a user interface to git.  Our git porcelain will be a pretty close
clone of the functionality and interface of the official git, except with
less features.


Git's UI (A Primer)
-------------------

Before we move on to implementation, let's take a moment to examine what the
current git interface is.

`git` is the primary entrypoint to the git command line interface.  To do
anything with git you must first type `git` at the prompt.  If we type only
`git` we get back a usage message and a list of subcommands:


.. code-block:: bash

    $ git
    usage: git [--version] [--help] [-C <path>] [-c name=value]
               [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
               [-p|--paginate|--no-pager] [--no-replace-objects] [--bare]
               [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
               <command> [<args>]

    The most commonly used git commands are:
       add        Add file contents to the index
       bisect     Find by binary search the change that introduced a bug
       branch     List, create, or delete branches
       checkout   Checkout a branch or paths to the working tree
       clone      Clone a repository into a new directory
       commit     Record changes to the repository
       diff       Show changes between commits, commit and working tree, etc
       fetch      Download objects and refs from another repository
       grep       Print lines matching a pattern
       init       Create an empty Git repository or reinitialize an existing one
       log        Show commit logs
       merge      Join two or more development histories together
       mv         Move or rename a file, a directory, or a symlink
       pull       Fetch from and integrate with another repository or a local branch
       push       Update remote refs along with associated objects
       rebase     Forward-port local commits to the updated upstream head
       reset      Reset current HEAD to the specified state
       rm         Remove files from the working tree and from the index
       show       Show various types of objects
       status     Show the working tree status
       tag        Create, list, delete or verify a tag object signed with GPG

    'git help -a' and 'git help -g' lists available subcommands and some
    concept guides. See 'git help <command>' or 'git help <concept>'
    to read about a specific subcommand or concept.

A couple of things stand out here. First, in the ``usage:`` message, we can see
that git has a number of optional arguments we can pass it directly.  For
instance one of those is ``--version``.

.. code-block:: bash

    $ git --version
    git version 2.1.4

These are often also called "flags", or "keyword arguments", especially when
used as ``-v`` and ``--version``, respectively.  Flags/Keyword arguments may
also be either optional or required.

The next, and probably most obvious thing, is the big list of commands.
Commands, are also known as "subcommands" and the term is often used
interchangably.  A great example of this is the last paragraph, where git
refers to the list as both "command" and "subcommand" in the same sentence.

    'git help -a' and 'git help -g' lists available subcommands and some
    concept guides. See 'git help <command>' or 'git help <concept>'
    to read about a specific subcommand or concept.

To round out our vocabulary (which now includes "flags/keyword arguments",
"optional/required arguments", "commands", and "subcommands"), we should
mention one other concept not seen here, which is "positional arguments".  A
positional argument is an argument (which may be either required or optional)
that comes directly after a command or flag/keyword argument.  A common example
of this in git is.

.. code-block:: bash

    $ git checkout -h
    usage: git checkout [options] <branch>

Here you can see that ``<branch>`` is a positional argument (also a required
one).

Git doesn't just stop at one level of subcommands though.  Some subcommands
have their own sets of subcommands!  

.. code-block:: bash

   $ git remote -h
   usage: git remote [-v | --verbose]
      or: git remote add [-t <branch>] [-m <master>] [-f] [--tags|--no-tags] [--mirror=<fetch|push>] <name> <url>
      or: git remote rename <old> <new>
      or: git remote remove <name>
      #...

In the example above, ``add``, ``rename``, and ``remove`` are each subcommands
to the subcommand ``remote``, which is a subcommand to the ``git`` command.

Clams exists to make building these types of nested command line tools, simple,
easy and maybe even fun!


Getting Started
---------------

Okay, now that we've taken a brief moment to examine git's interface and some
of the common concepts behind command line interface design, let's jump right
into building our own!


