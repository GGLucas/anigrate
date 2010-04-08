from __future__ import print_function

import datetime

from anigrate.display.loglist import LogDisplay
from anigrate.models import Session, Series, Season, Watched
from anigrate.util import register, selector, arguments, debug, checkint, verbose, paranoia, parsedate, interactive_selector

RELATIVE, ABSOLUTE, BOTH = range(0,3)

@register("watch", shorthelp="add an entry to the watch log")
@arguments(1,3)
@selector
@interactive_selector
@paranoia(2)
def cm_watch(selector, num=None, date=None):
    """
    watch [num] [date]: [selector]
        Add an entry to the series watch log for all series matching [selector].
        If no [num] is specified anigrate acts as if one additional episode was 
        watched in the current season. If [date] is specified the watch log 
        entries will have their watch dates set to this instead of the current
        date and time.

        [num] can be specified in various formats:

          [+-]x  :  Add or remove x episodes to the watched count.
                    Note that watch log entries can be lost if the count
                    is decreased beyond their starting position.
                     Examples: +1 +3 -1 -4

          x      :  Set the watched count to exactly x, adding and removing
                    log entries as necessary.
                     Examples: 5 12 24

          x/y    :  Set the watched count to exactly x, and simultaneously
                    set the current season's length to y.
                     Examples: 5/12 13/24 16/20

          x/, /x :  Set the watched count to exactly x, and simultanously
                    set the current season's length to x as well. In other 
                    words, this marks the season as completed with x eps.
                     Examples: 14/ 22/ /26 /52

        See `help dates` for acceptable date formats.
    """

    # Parse date
    if date is not None:
        date = parsedate(date)
    else:
        date = datetime.datetime.now()

    # Parse watched count
    if num is not None:
        if num[0] in ('+', '-'):
            mode = RELATIVE
            num = (-1 if num[0] == '-' else 1) * checkint(num[1:],
             "wachted count")
        elif '/' in num:
            mode = BOTH
            ep, total = num.split('/')

            if ep and total:
                num = checkint(ep, "watched count")
                total = checkint(total, "total episodes")
            elif ep:
                num = total = checkint(ep, "watched count")
            elif total:
                num = total = checkint(total, "watched count")
            else:
                debug("Error: watched count is in an invalid format.", False)
        else:
            mode = ABSOLUTE
            num = checkint(num, "watched count")
    else:
        mode = RELATIVE
        num = 1

    # Execute
    for series in selector.all_all():
        # Set length
        if mode == BOTH:
            series.epstotal = total
            series.current_season.episode_total = total

        # Set episode
        if mode == RELATIVE:
            num = series.epscurrent+num

        # Adapt watch log
        if num > series.epscurrent:
            if num <= series.epstotal or series.epstotal == 0:
                log = Watched(
                    seasonnum=series.current,
                    season=series.current_season,
                    series=series,
                    time=date,
                    startep=series.epscurrent,
                    finishep=num
                )
                Session.add(log)
            else:
                print("Error: watched count is larger than total season length"
                " for series `%s`.." % series.title)
                continue
        elif num < series.epscurrent:
            if num >= 0:
                for entry in series.watched:
                    if entry.startep >= num:
                        Session.delete(entry)
                    elif entry.finishep > num:
                        entry.finishep = num
            else:
                print("Error: watched count is smaller than 0"
                " for series `%s`.." % series.title)
                continue

        # Adapt watched counts
        series.epscurrent = num
        series.current_season.current_watched = num
        series.eval_finished()

    Session.commit()

    # Display log
    LogDisplay(selector=selector).output(print=lambda text: print("  "+text))
