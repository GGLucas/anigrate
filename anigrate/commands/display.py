from __future__ import print_function

from anigrate.config import Config
from anigrate.util import (register, selector, arguments, checkint, parsedate,
                          showdate, showtime, rating_color)
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
    ListDisplay(selector=selector).output(
        print=lambda text: print("  " + text))


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

    LogDisplay(selector=selector, limit=limit).output(
        print=lambda text: print("  " + text))


@register("history", shorthelp="display watch history")
@arguments(1, 3)
@selector
def cm_hist(selector, limit=None, date=None):
    """
    hist [num] [date]: [selector]
        Show the last [num] watched episode entries for series matching
        [selector]. If [date] is specified, ignore any entries more recent
        than [date].

        Num defaults to the value specified in the configuration.
        Matches all series if no selector is specified.

        See `help dates` for acceptable date formats.
    """
    if date is not None:
        date = parsedate(date)

    HistDisplay(selector=selector, limit=limit, date=date).output(
        print=lambda text: print("  " + text))


@register("get", shorthelp="get all series information")
@arguments(1)
@selector
def cm_get(selector):
    """
    get: [selector]
        Show all recorded information about a series and its seasons.
        Does not show the watch log (use `log` for that)
    """
    ## TODO: If selector is empty, show incremental switch

    ATTRIBUTES = (
        ('ID', lambda s: ('normal', str(s.id))),
        ('Category', lambda s: ('normal', s.category or "None")),
        ('Duration', lambda s: ('normal', str(s.duration) + 
                                          " min/episode ")),
        ('Rating', lambda s: (rating_color(s.rating), str(s.rating or "??"))),
        ('Dropped', lambda s: ("series_dropped", "Yes") if s.dropped else
                              ("series_normal", "No")),
        ('Finished', lambda s: ("series_normal", "Yes") if s.finished else
                              ("series_watching", "No")),
        ('Season', lambda s: ('normal', str(s.current))),
        ('Created', lambda s: ('normal', showdate(s.ctime) + " " +
                                         showtime(s.ctime))),
        ('Modified', lambda s: ('normal', showdate(s.mtime) + " " +
                                          showtime(s.mtime))),
    )

    for series in selector.season_all():
        print(" " + Config.color('header', series.title))

        for attr in ATTRIBUTES:
            print("  " + Config.multicolor(*('itemname', attr[0].ljust(12),) +
                         attr[1](series)))

        print()

        for season in series.seasons:
            print("   " + Config.multicolor(
                "normal", "Season ", 
                "seasonnum", str(season.num),
                "normal", ":    ",
                "epcount" if season.current_watched == season.episode_total
                          else "normal",
                    str(season.current_watched),
                "normal", " / ",
                "epcount", str(season.episode_total or "??"),
                ))

        print()
