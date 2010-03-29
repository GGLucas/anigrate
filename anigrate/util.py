import sys

from anigrate.config import Config

Commands = {}
Commands_Order = []
Commands_Season = {}

def choose(values, name, first_only=False, key_only=False,
                         allow_multi=True, value_only=False):
    """
        Choose a value from a dictionary with a uniquely specified
        but not complete key.
    """
    match = []

    # Get all matching
    for key, value in values.items():
        if key.startswith(name):
            match.append((key, value))

    # Check if multiple matches are allowed
    if not allow_multi and len(match) > 1:
        return None

    # Check if we should strip out keys or values
    if key_only:
        match = [m[0] for m in match]
    elif value_only:
        match = [m[1] for m in match]

    # Check if we should collapse the list
    if first_only or not allow_multi:
        return match[0]
    else:
        return match

def register(name=None, dictionary=None, sortorder=None, **kwargs):
    """
        Register a function as a command.
    """
    def cmd(func):
        # Get dictionary to add this command to
        if dictionary is None:
            global Commands, Commands_Order
            cm = Commands
            order = Commands_Order
        else:
            cm = dictionary
            order = sortorder

        # Set extra function properties
        for key, value in kwargs.items():
            setattr(func, key, value)

        # Set command in the dictionary
        cm[name or func.__name__] = func

        # Append to sort order
        if order is not None:
            order.append(name or func.__name__)

        return func

    return cmd

def selector(func):
    """
        Mark function as requiring a prepared selector.
    """
    func.selector = 1
    return func

def selector_literal(func):
    """
        Mark function as requiring a literal selector.
    """
    func.selector = 2
    return func

def arguments(minargs=0, maxargs=None):
    """
        Specify the minimum and/or maximum amount of arguments
        this function can take.
    """
    def cmd(func):
        func.minargs = minargs
        func.maxargs = minargs if maxargs is None else maxargs
        return func
    return cmd

def debug(error, raise_exception=True):
    """
        Either print a stack trace when in debug mode or raise an error message.
        If no stack trace is available, just raise the error.
    """
    if Config.debug and raise_exception:
        raise
    else:
        print(error)
        sys.exit(1)

def checkint(var, name="", exit=True):
    """
        Check if a variable is parseable as an integer.
        Return the integer if it is or display an error if it's not.
    """
    # If it's none, pass through
    if var is None:
        return None

    # Try to convert to int
    try:
        return int(var)
    except ValueError:
        print("Error: %s is not a valid integer." % name)
        if exit: sys.exit(1)

def promptfor(prompt, default=None, allow_empty=False):
    """
        Prompt for a value to be entered, or use a default.
    """

    # Prompt
    if default is not None:
        value = raw_input("%s [%s]: " % (prompt, default))
    else:
        value = raw_input("%s: " % prompt)

    # Set default
    if value == "." or (not value and default and not allow_empty):
        value = default

    return value

def verbose(line, level=1):
    """
        Only display a line when verbosity allows it.
    """
    if not Config.quiet:
        print(line)
