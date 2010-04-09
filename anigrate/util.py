from __future__ import print_function

import sys
import datetime

from anigrate.models import Series
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

def lcrop(string, size):
    """ Resize a string to fit in size. """
    if len(string) <= size:
        return string.ljust(size)
    else:
        return string[:size - 2]+".."

def rcrop(string, size):
    """ Resize a string to fit in size from the right. """
    if len(string) <= size:
        return string.rjust(size)
    else:
        return string[:size - 2]+".."

def fuzzymatch(string, target, caseinsensitive=True):
    """ Calculate fuzzy match score between two series. """
    if caseinsensitive:
        string = string.lower()

    # Perfect match
    if string == target or not target:
        return (1.0, [])

    # Calculate offsets
    strlen = len(string)
    offsets = []
    cursor = 0

    for char in target:
        i = 0
        found = False
        while cursor < strlen:
            if char == string[cursor]:
                offsets.append(i)
                cursor += 1
                found = True
                break

            cursor += 1
            i += 1
        if found:
            continue
        return (0.0, [])

    # Calculate score
    score = 0.0
    maxcharscore = 1.0/len(target)
    cursor = 0

    for offset in offsets:
        factor = 1.0

        if offset > 0:
            last = string[offset-1]

            if last == ' ':
                factor = 0.9
            else:
                factor = 1.0/(offset+1)

        score += maxcharscore*factor

    return (score, offsets)

def fuzzyselect(selector):
    """ Display a selector prompt. """
    import curses
    curses.setupterm()
    clear = curses.tigetstr("el")
    clearall = curses.tigetstr("ed")
    up = curses.tigetstr("cuu1")
    down = curses.tigetstr("cud1")
    rev = curses.tigetstr("rev")
    sgr0 = curses.tigetstr("sgr0")
    char = curses.tigetstr("hpa")
    zero = curses.tparm(char, 0)

    import tty
    import termios
    import fcntl
    import os
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    series = selector.all()
    subset = series[:]
    selected = 0
    scroll = 0
    amount = Config.getint("anigrate", "matcher_items")

    try:
        tty.setraw(fd)
        filt = ""
        next = True

        while True:
            # Build list
            num = 0
            sys.stdout.write(zero + clear+"series> " + 
                             filt)

            for i, s in enumerate(subset[scroll:scroll + amount]):
                data = (" " + lcrop(s.title, 50) + " " +
                           rcrop(str(s.epscurrent),3) + " / " +
                           rcrop(str(s.epstotal), 3) +
                           rcrop(s.category, 10) + " ")
                if i == selected - scroll:
                    sys.stdout.write(down + zero + clear +
                                     rev + data + sgr0)
                else:
                    sys.stdout.write(down + zero + clear + data)
                num += 1

            # Set cursor
            sys.stdout.write((down+zero+clear)*(amount-num))
            sys.stdout.write(up*amount+curses.tparm(char, len(filt)+8))

            # Wait for next character
            next = sys.stdin.read(1)

            if next == "\r":
                # Stop searching
                break
            else:
                # Expand filter
                reval = False
                if next == "\x7f":
                    # Backspace
                    if filt:
                        filt = filt[:-1]
                        reval = True
                elif next == "\x03":
                    # Control+c
                    return
                elif next == "\x1b":
                    # Cursor key
                    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
                    fcntl.fcntl(fd, fcntl.F_SETFL, flags|os.O_NONBLOCK)
                    try:
                        next = sys.stdin.read(2)
                    except IOError:
                        # Escape pressed
                        return
                    fcntl.fcntl(fd, fcntl.F_SETFL, flags)

                    if next == "[A":
                        # Up
                        selected -= 1

                        if selected < 0:
                            selected = len(subset) - 1
                            scroll = selected - amount+1

                            if scroll < 0:
                                scroll = 0
                        elif selected < scroll:
                            scroll -= 1
                    elif next == "[B":
                        # Down
                        selected += 1

                        if selected >= len(subset):
                            selected = 0
                            scroll = 0
                        elif selected >= scroll + amount:
                            scroll += 1
                else:
                    filt += next
                    reval = True

                if reval:
                    case = (filt == filt.lower())
                    subset = map(lambda s: (fuzzymatch(s.title, filt, case), s), series)
                    subset = filter(lambda s: s[0][0] != 0.0, subset)
                    subset = sorted(subset, key=lambda s: s[0][0], reverse=True)
                    subset = map(lambda s: s[1], subset)
                    selected = 0

    finally:
        sys.stdout.write(zero+clearall)
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    if subset:
        return Series.id == subset[selected].id
    else:
        return

def interactive_selector(func):
    """ Display interactive selector when called with an empty selector. """
    def cmd(*args, **kwargs):
        selector = args[0]

        if not selector.filters and \
           Config.getboolean("anigrate", "matcher_enabled"):
            filt = fuzzyselect(selector)

            if filt is None:
                return
            else:
                selector.filters.append(filt)

        return func(*args, **kwargs)
    cmd.__name__ = func.__name__
    cmd.__doc__ = func.__doc__
    return cmd
