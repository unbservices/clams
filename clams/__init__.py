"""
Clams
=====

Create simple, nested, command-line interfaces.


Example
-------

A simple example with one `hello` sub-command.  This can be found at
/demo/salutation.py.


    from clams import arg, Command

    salutation = Command('salutation')

    @salutation.register('hello')
    @arg('name', nargs='?')  # <== same interface as argparse's `add_argument`
    def handler(name):
        print 'Hello %s' % name or 'Nick'

    @salutation.register('goodbye')
    @arg('name', nargs='?')
    def handler(name):
        print 'Goodbye %s' % name or 'Nick'

    if __name__ == '__main__':
        root.init()
        root.parse_args()


Usage:

    $ cd demo

    $ ./salutation.py hello
    Hello Nick

    $ ./salutation.py hello Jason
    Hello Jason

    $ ./salutation.py goodbye "my friend."
    Goodbye my friend.


For more in-depth examples, see the /demo directory.

"""

import argparse


def arg(*args, **kwargs):
    """Annotate a function by adding an Argparse arg to the meta-data.

    This appends an Argparse "argument" to the function's ``ARGPARSE_ARGS_LIST``
    attribute, creating ``ARGPARSE_ARGS_LIST`` if it does not already exist.
    Aside from that, it returns the decorated function unmodified, and unwrapped.

    The "arguments" are simply ``(args, kwargs)`` tuples which will be passed to
    the parser created from the function as
    ``parser.add_argument(*args, **kwargs)``.

    Args:

      name/flags -  Either a name or a list of (positional) option strings,
                    e.g. ('foo') or ('-f', '--foo').
      action     -  The basic type of action to be taken when this argument is
                    encountered at the command line.
      nargs      -  The number of command-line arguments that should be
                    consumed.
      const      -  A constant value required by some action and nargs
                    selections.
      default    -  The value produced if the argument is absent from the
                    command line.
      type       -  The type to which the command-line argument should be
                    converted.
      choices    -  A container of the allowable values for the argument.
      required   -  Whether or not the command-line option may be omitted
                    (optionals only).
      help       -  A brief description of what the argument does.
      metavar    -  A name for the argument in usage messages.
      dest       -  The name of the attribute to be added to the object
                    returned by parse_args().


    Example:

        @arg('-n', '--num', type=int, default=42)
        @arg('-s', '--some-switch', action='store_false')
        def command_name(args):
          print 'args: ', args


    Also see:

      [argparse.add_argument](
        https://docs.python.org/2/library/argparse.html#the-add-argument-method)
    """
    def annotate(func):
        # Get the list of argparse args already added to func (if any).
        argparse_args_list = getattr(func, 'ARGPARSE_ARGS_LIST', [])
        argparse_args_list.insert(0, (args, kwargs))
        setattr(func, 'ARGPARSE_ARGS_LIST', argparse_args_list)
        return func
    return annotate


def command(name):
    def wrapper(func):
        command = Command(name)
        command.add_handler(func)
        argparse_args_list = getattr(func, 'ARGPARSE_ARGS_LIST', [])
        for args, kwargs in argparse_args_list:
            command.add_arg_tuple((args, kwargs))
        return command
    return wrapper


def register(command):
    def wrapper(subcommand):
        command.add_command(subcommand)
        return subcommand
    return wrapper


def register_command(parent_command, name):
    def wrapper(func):
        c = command(name)(func)
        parent_command.add_command(c)
    return wrapper


class Command(object):
    def __init__(self, name):
        self.name = name
        self.registered_arguments = []
        self.registered_commands = []
        self.handler = None

        # The following attributes are constructed by `self.register`

        # Command passed to `self.register` or argparse.ArgumentParser() if Command
        # is None (only on root).
        self.command = None
        self.subparsers = None  # self.command.add_subparsers()

    def add_arg(self, *args, **kwargs):
        self.registered_arguments.append((args, kwargs))

    def add_arg_tuple(self, arg_tuple):
        self.registered_arguments.append(arg_tuple)

    def add_command(self, command):
        self.registered_commands.append(command)
        return command

    def add_handler(self, handler):
        self.handler = handler


    def attach_registered_arguments(self):
        for arg in self.registered_arguments:
            self.command.add_argument(*arg[0], **arg[1])

    def attach_registered_commands(self):
        if self.registered_commands:
            self.subparsers = self.command.add_subparsers()

            for registered_command in self.registered_commands:
                subparser = self.subparsers.add_parser(registered_command.name)
                if registered_command.handler:
                    subparser.set_defaults(_func=registered_command.handler)
                registered_command.init(subparser)


    def init(self, command=None):
        if self.command is None:
            if command is None:
                self.command = argparse.ArgumentParser()
            else:
                self.command = command

        self.attach_registered_arguments()
        self.attach_registered_commands()


    def parse_args(self):
        parsed = self.command.parse_args()
        if hasattr(parsed, '_func'):
            _func = parsed._func
            del parsed._func
            return _func(**vars(parsed))
        else:
            print 'Command not found'
            print 'parsed: ', parsed

    def register_command(self, name):
        return register_command(self, name)

    def register(self, name=None):
        if name is None:
            return register(self)
        else:
            return self.register_command(name)
