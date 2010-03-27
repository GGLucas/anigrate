from __future__ import print_function

from anigrate.util import register, selector, arguments, checkint
from anigrate.display.serieslist import ListDisplay
from anigrate.display.loglist import LogDisplay

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
