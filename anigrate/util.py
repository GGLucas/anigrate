import sys

from anigrate.config import Config

Commands = {}
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

def register(name=None, dictionary=None):
    """
        Register a function as a command.
    """
    def cmd(func):
        # Get dictionary to add this command to
        if not dictionary:
            global Commands
            cm = Commands
        else:
            cm = dictionary

        # Set command in the dictionary
        cm[name or func.__name__] = func
        return func

    return cmd

def selector(func):
    """
        Mark function as requiring a prepared selector.
    """
    func.selector = True
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
