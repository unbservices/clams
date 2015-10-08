"""
Clams
=====

Create simple, nested, command-line interfaces.


Example
-------

A simple example with ``hello`` and ``goodbye`` subcommands.  This can be found
at `/demo/salutation.py </demo/salutation.py>`_.

.. testcode::

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
       salutation.init()
       salutation.parse_args()

Usage:

.. code-block:: console

   $ cd demo

   $ ./salutation.py hello
   Hello Nick

   $ ./salutation.py hello Jason
   Hello Jason

   $ ./salutation.py goodbye "my friend."
   Goodbye my friend.


For more in-depth examples, see the `/demo </demo>`_ directory.

.. doctest::
   :hide:

   >>> salutation.init()
   >>> salutation.parse_args(['hello', 'Bob'])
   Hello Bob
   >>> salutation.parse_args(['goodbye', 'Alice'])
   Goodbye Alice

"""

import argparse
import textwrap


def arg(*args, **kwargs):
    """Annotate a function by adding the args/kwargs to the meta-data.

    This appends an Argparse "argument" to the function's
    ``ARGPARSE_ARGS_LIST`` attribute, creating ``ARGPARSE_ARGS_LIST`` if it
    does not already exist.  Aside from that, it returns the decorated function
    unmodified, and unwrapped.

    The "arguments" are simply ``(args, kwargs)`` tuples which will be passed
    to the Argparse parser created from the function as
    ``parser.add_argument(*args, **kwargs)``.

    `argparse.ArgumentParser.add_argument
    <https://docs.python.org/2/library/argparse.html#the-add-argument-method>`_
    should be consulted for up-to-date documentation on the accepted arguments.
    For convenience, a list has been included here.

    Args
    ----
    name/flags : str or list
        Either a name or a list of (positional) option strings, e.g. ('foo') or
        ('-f', '--foo').
    action : str
        The basic type of action to be taken when this argument is encountered
        at the command line.
    nargs : str
        The number of command-line arguments that should be consumed.
    const
        A constant value required by some action and nargs selections.
    default
        The value produced if the argument is absent from the command line.
    type : type
        The type to which the command-line argument should be converted.
    choices
        A container of the allowable values for the argument.
    required : bool
        Whether or not the command-line option may be omitted (optionals only).
    help : str
        A brief description of what the argument does.
    metavar : str
        A name for the argument in usage messages.
    dest : str
        The name of the attribute to be added to the object returned by
        parse_args().

    Example
    -------
    .. testsetup::

       mycommand = Command(name='mycommand')

    .. testcode::

        @command(name='echo')
        @arg('-n', '--num', type=int, default=42)
        @arg('-s', '--some-switch', action='store_false')
        @arg('foo')
        def echo(foo, num, some_switch):
            print foo, num

    .. doctest::

       >>> echo_subcommand = mycommand.add_subcommand(echo)
       >>> mycommand.init()
       >>> mycommand.parse_args(['echo', 'hi', '-n', '42'])
       hi 42

    See also
    --------
    `argparse.ArgumentParser.add_argument
    <https://docs.python.org/2/library/argparse.html#the-add-argument-method>`_

    """
    def annotate(func):
        # Get the list of argparse args already added to func (if any).
        argparse_args_list = getattr(func, 'ARGPARSE_ARGS_LIST', [])
        # Since we're only annotating (not wrapping) the function, appending
        # the argument to the list would result in the decorators being applied
        # in reverse order.  To prevent that, we simply add to the beginning.
        argparse_args_list.insert(0, (args, kwargs))
        setattr(func, 'ARGPARSE_ARGS_LIST', argparse_args_list)
        return func
    return annotate


def _parse_doc(doc=''):
    """Parse a docstring into title and description.

    Args
    ----
    doc : str
        A docstring, optionally with a title line, separated from a description
        line by at least one blank line.

    Returns
    -------
    title : str
        The first line of the docstring.
    description : str
        The rest of a docstring.

    """
    title, description = '', ''
    if doc:
        sp = doc.split('\n', 1)
        title = sp[0].strip()
        if len(sp) > 1:
            description = textwrap.dedent(sp[1]).strip()
    return (title, description)


def command(name):
    """Create a command, using the wrapped function as the handler.

    Args
    ----
    name : str
        Name given to the created Command instance.

    Returns
    -------
    Command
        A new instance of Command, with handler set to the wrapped function.

    """
    # TODO(nick): It would be nice if this didn't transform the handler.  That
    #   way, handlers could be used and tested independently of this system.
    #   Unfortunately that's one of the better properties of the previous
    #   system that wasn't preserved in this rewrite.
    def wrapper(func):
        title, description = _parse_doc(func.__doc__)
        command = Command(name=name, title=title, description=description)
        command.add_handler(func)
        argparse_args_list = getattr(func, 'ARGPARSE_ARGS_LIST', [])
        for args, kwargs in argparse_args_list:
            command.add_argument_tuple((args, kwargs))
        return command
    return wrapper


def register(command):
    """Register a command with a parent command.

    The ``register`` decorator decorates a Command instance (not a function).
    It is intended to be used with the ``command`` decorator (which decorates a
    function and returns a Command instance).

    Args
    ----
    comand : Command
        The parent command.

    Example
    -------
    .. testcode::

       mygit = Command(name='status')

       @register(mygit)
       @command('status')
       def status():
           print 'Nothing to commit.'

    .. doctest::
       :hide:

       >>> mygit.init()
       >>> mygit.parse_args(['status'])
       Nothing to commit.

    """
    def wrapper(subcommand):
        command.add_subcommand(subcommand)
        return subcommand
    return wrapper


def register_command(parent_command, name):
    """Create and register a command with a parent command.

    Args
    ----
    parent_comand : Command
        The parent command.
    name : str
        Name given to the created Command instance.

    Example
    -------
    .. testcode::

       mygit = Command(name='status')

       @register_command(mygit, 'status')
       def status():
           print 'Nothing to commit.'

    .. doctest::
       :hide:

       >>> mygit.init()
       >>> mygit.parse_args(['status'])
       Nothing to commit.

    """
    def wrapper(func):
        c = command(name)(func)
        parent_command.add_subcommand(c)
    return wrapper


class Command(object):
    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title
        self.description = description

        self.arguments = []
        self.subcommands = []
        self.handler = None
        self.parser = None
        self.initialized = False  # has the _init method been called?

    def add_argument_tuple(self, arg_tuple):
        """Add a new argument to this Command.

        Args
        ----
        arg_tuple : tuple
            A tuple of ``(*args, **kwargs)`` that will be passed to
            ``argparse.ArgumentParser.add_argument``.

        """
        self.arguments.append(arg_tuple)

    def add_subcommand(self, command):
        """Add a new subcommand to this Command.

        Args
        ----
        command : Command
            The Command instance to add.

        """
        self.subcommands.append(command)
        return command

    def add_handler(self, handler):
        """Add a handler to be called with the parsed argument namespace.

        Args
        ----
        handler : function
            A function that accepts the arguments defined for this command.

        """
        self.handler = handler

    def _register_handler(self, subparser, handler):
        """Add a handler as a default ``_func`` attribute to a subparser.

        Args
        ----
        subparser : argparse.ArgumentParser
            The subparser to add the handler to.
        handler : function
            The function to add to the subparser, which will be called with the
            namespace returned by the subparser as kwargs.

        Returns
        -------
        None

        """
        subparser.set_defaults(_func=handler)

    def _get_handler(self, namespace, remove_handler=False):
        """Get a handler (if present) from a namespace.

        Returns
        -------
        function or None
            The handler defined in the namespace.

        """
        if hasattr(namespace, '_func'):
            _func = namespace._func
            if remove_handler:
                del namespace._func
            return _func

    def _attach_arguments(self):
        """Add the registered arguments to the parser."""
        for arg in self.arguments:
            self.parser.add_argument(*arg[0], **arg[1])

    def _attach_subcommands(self):
        """Create a subparser and add the registered commands to it.

        This will also call ``_init`` on each subcommand (in turn invoking its
        ``_attach_subcommands`` method).
        """
        if self.subcommands:
            self.subparsers = self.parser.add_subparsers()

            for subcommand in self.subcommands:
                subparser = self.subparsers.add_parser(subcommand.name,
                                                       help=subcommand.title)
                if subcommand.handler:
                    self._register_handler(subparser, subcommand.handler)
                subcommand._init(subparser)

    def _init(self, parser):
        """Initialize/Build the ``argparse.ArgumentParser`` and subparsers.

        This internal version of ``init`` is used to ensure that all
        subcommands have a properly initialized parser.

        Args
        ----
        parser : argparse.ArgumentParser
            The parser for this command.

        """
        assert isinstance(parser, argparse.ArgumentParser)
        self._init_parser(parser)

        self._attach_arguments()
        self._attach_subcommands()
        self.initialized = True

    def _init_parser(self, parser):
        self.parser = parser
        self.parser.title = self.title
        self.parser.description = self.description
        self.parser.formatter_class = argparse.RawDescriptionHelpFormatter

    def init(self):
        """Initialize/Build the ``argparse.ArgumentParser`` and subparsers.

        This must be done before calling the ``parse_args`` method.
        """
        parser = argparse.ArgumentParser()
        self._init(parser)

    def parse_args(self, args=None, namespace=None):
        """Parse the command-line arguments and call the associated handler.

        The signature is the same as `argparse.ArgumentParser.parse_args
        <https://docs.python.org/2/library/argparse.html#argparse.ArgumentParser.parse_args>`_.

        Args
        ----
        args : list
            A list of argument strings.  If ``None`` the list is taken from
            ``sys.argv``.
        namespace : argparse.Namespace
            A Namespace instance.  Defaults to a new empty Namespace.

        Returns
        -------
        The return value of the handler called with the populated Namespace as
        kwargs.

        """
        assert self.initialized, '`init` must be called before `parse_args`.'
        namespace = self.parser.parse_args(args, namespace)
        handler = self._get_handler(namespace, remove_handler=True)
        if handler:
            return handler(**vars(namespace))

    # Decorators
    # ----------

    def register_command(self, name):
        """Decorator to create and register a command from a function.

        Args
        ----
        name : str
            The name given to the registered command.

        Example
        -------
        .. testcode::

           mygit = Command(name='mygit')

           @mygit.register_command(name='status')
           def status():
               print 'Nothing to commit.'

        .. doctest::
           :hide:

           >>> mygit.init()
           >>> mygit.parse_args(['status'])
           Nothing to commit.

        """
        return register_command(self, name)

    def register(self, name=None):
        """Decorator to (create and) register a command from a function.

        Args
        ----
        name : Optional[str]
            If present, create a command and register it (see
            ``register_command``).

        Example
        -------
        .. testcode::

           mygit = Command(name='status')

           @mygit.register(name='status')
           def status():
               print 'Nothing to commit.'

           @mygit.register()
           @command(name='log')
           def log():
               print 'Show logs.'

        .. doctest::
           :hide:

           >>> mygit.init()
           >>> mygit.parse_args(['status'])
           Nothing to commit.

           >>> mygit.parse_args(['log'])
           Show logs.

        """
        if name is None:
            return register(self)
        else:
            return self.register_command(name)
