from __future__ import print_function

from anigrate.util import register, selector, arguments, checkint
from anigrate.display.serieslist import ListDisplay
from anigrate.display.loglist import LogDisplay
from anigrate.display.histlist import HistDisplay

@register("list", shorthelp="display a list of series")
@arguments(1)
@selector
def cm_list(selector):
    """
    list: [selector]
        List all series matched by [selector].
        If no selector is given, match all series.
    """
    ListDisplay(selector=selector).output(print=lambda text: print("  "+text))

@register("log", shorthelp="display series watch log")
@arguments(1, 2)
@selector
def cm_log(selector, limit=None):
    """
    log [limit]: [selector]
        Show a detailed log for series matching [selector].
        If limit is specified, limit the amount of log entries shown per
        matched series to that number.
    """
    limit = checkint(limit, "limit argument")

    LogDisplay(selector=selector, limit=limit).output(print=lambda text: print("  "+text))

@register("history", shorthelp="display watch history")
@arguments(1, 3)
@selector
def cm_hist(selector, limit=None, time=None):
    """
    hist [num] [time]: [selector]
        Show the last [num] watched episode entries for series matching
        [selector]. If [time] is specified, ignore any entries more recent 
        than [time] days in the past.

        Num defaults to the value specified in the configuration.
        Matches all series if no selector is specified.
    """
    limit = checkint(limit, "limit argument")
    time = checkint(time, "time argument")

    HistDisplay(selector=selector, limit=limit, time=time).output(print=lambda text: print("  "+text))
