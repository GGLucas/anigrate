import sys
import datetime

from anigrate.config import Config

try:
    import dateutil.parser
    HAVE_DATEUTIL = True
except ImportError:
    HAVE_DATEUTIL = False

Commands = {}
Commands_Order = []
Commands_Season = {}
Commands_Season_Order = []

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

def paranoia(level, verb="modify", count=1, complete=False):
    """
        Specify the paranoia level on this function. If the function
        paranoia is higher than the configured paranoia, alert the user
        when the function will act on more than [count] items.
    """
    system = "[yes/NO]" if complete else "[y/N]"

    def decor(func):
        def cmd(*args, **kwargs):
            if Config.getint("anigrate", "paranoia") >= level:
                selector = args[0]
                amount = selector.count()

                if amount > count:
                    prompt = raw_input("You are about to %s %d series, are you"
                    " absolutely sure %s? " % (verb, amount, system)).lower()

                    if complete:
                        if prompt != "yes":
                            if prompt and "yes".startswith(prompt):
                                print("Please type 'yes' completely at the prompt.")
                            return
                    elif not "yes".startswith(prompt):
                            return
            func(*args, **kwargs)
        cmd.__name__ = func.__name__
        cmd.__doc__ = func.__doc__
        return cmd
    return decor

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
        else: return None

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

def parseprogress(progress, exit=True):
    """
        Parse progress string to a list of (current, total) tuples.
    """
    if progress:
        seasons = []

        for season in progress.split(","):
            # Amount of seasons to create like this
            if "*" in season:
                season, times = season.split("*", 1)
                times = checkint(times, "season multiplier", exit)
            else:
                times = 1

            # Watched and total
            if "/" in season:
                watched, total = season.split("/")

                if watched:
                    watched = checkint(watched, "watched amount", exit)
                else:
                    watched = checkint(total, "total episodes", exit)

                if total:
                    total = checkint(total, "total episodes", exit)
                else:
                    total = watched
            else:
                watched = checkint(season, "watched amount", exit)
                total = 0

            seasons.extend([(watched, total),]*times)
    else:
        seasons = ((0, 0),)

    return seasons

def parsedate(string, error=True):
    """
        Attempt to parse a date string using the method available.
    """
    if HAVE_DATEUTIL:
        try:
            return dateutil.parser.parse(string)
        except ValueError:
            pass
    else:
        try:
            return datetime.datetime.strptime(string, '%Y%m%d')
        except ValueError:
            pass

    if error:
        debug("Error: date is in an unknown format.", False)
    else:
        return None

def showdate(datetime):
    """
        Display a date in default format.
    """
    return datetime.strftime(Config.get("appearance", "date_format"))

def showtime(datetime):
    """
        Display a date in default format.
    """
    return datetime.strftime(Config.get("appearance", "time_format"))

def rating_color(rating):
    """
        Get the color to display for a certain rating.
    """
    return [
            "unknown", "score_critical",
            "score_critical", "score_critical",
            "score_low", "score_low",
            "score_normal", "score_normal",
            "score_high", "score_high",
            "score_top",
        ][rating]

def interactive_selector(func):
    """ Display interactive selector when called with an empty selector. """
    return func #TODO: implement
