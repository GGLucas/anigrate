import datetime
from math import floor

from anigrate.models import Session, Series, Season, Watched
from anigrate.util import (register, selector, selector_literal,
                   arguments, promptfor, debug, checkint, verbose,
                   paranoia)

@register("time", shorthelp="get total watching time spent")
@arguments(1)
@selector
def cm_time(selector):
    """
    time: [selector]
        Get the total watching time spent on series matching [selector].
        If no selector is specified, the total watching time for all 
        series is given.
    """
    totalminutes, totaldays, times = selector.time

    print("Total time spent watching:")
    print("    %d years, %d months, %d weeks, %d days, %d hours, %d minutes" % tuple(times))
    print("")
    print("Or:")
    print("    %.1f total days = %d total minutes" % (totaldays, totalminutes))
    print("")
