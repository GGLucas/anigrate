import datetime
from anigrate.models import Session, Season, Watched
from anigrate.util import (register, arguments, selector, checkint,
                            verbose, promptfor, parseprogress,
                            paranoia, Commands_Season, parsedate,
                            Commands_Season_Order, interactive_selector)


@register("season", shorthelp="modify season information")
def cm_season():
    """
    season
        Modify various information about seasons. See the season
        command reference.
    """


@register("add", shorthelp="add a new season",
          dictionary=Commands_Season, sortorder=Commands_Season_Order)
@arguments(1, 3)
@selector
@interactive_selector
@paranoia(2)
def cm_season_add(selector, progress=None, seasonnum=None, date=None):
    """
    season add [watched[/total][*seasons],..] [number] [date]: [selector]
        Add new season(s) to specified series. Current progress for
        each season can be specified as the first argument.

        [number] specifies what the season number of the first season
        should be set to. If not given, [number] will default to the current
        season increased by one.
    """

    if date is not None:
        date = parsedate(date)
    else:
        date = datetime.datetime.now()

    seasons = parseprogress(progress)
    seasonnum = checkint(seasonnum, "season number")

    for series in selector.all():
        number = seasonnum or series.current + 1

        # Create every season
        for num, (current, total) in enumerate(seasons):
            # Season entry
            season = Season(
                num=num + number,
                series=series,
                episode_total=total,
                current_watched=current,
            )

            series.current = season.num
            Session.add(season)

            # Log entry
            if current > 0:
                watched = Watched(
                    season=season,
                    seasonnum=season.num,
                    series=series,
                    time=date,
                    startep=0,
                    finishep=current,
                )

                Session.add(watched)

            series.eval_finished()

    Session.commit()


@register("length", shorthelp="set season length",
          dictionary=Commands_Season, sortorder=Commands_Season_Order)
@arguments(1, 3)
@selector
@interactive_selector
@paranoia(2)
def cm_season_length(selector, value=None, seasonnum=None):
    """
    season length [length] [season]: (selector)
        Set the length in episodes for season [season].

        If [season] is not given, set length for the active season.
    """

    value = checkint(value, "rating")
    seasonnum = checkint(seasonnum, "season number")

    for series in selector.all():
        orig = series.epstotal

        if seasonnum is None:
            seasonnum = series.current

        # Prompt if not given
        if value is None:
            # Prompt
            new = promptfor("Enter new length for season %d of series `%s`" %
            (seasonnum, series.title), orig)

            # Convert to number
            new = checkint(new, "length", exit=False)

            if new == None:
                continue
        else:
            new = value

        if series.rating != new and value is not None:
            verbose("Setting length to %d for season %d of %s..." %
                      (new, seasonnum, series.title))

        series.epstotal = new
        series.season_bynum(seasonnum).episode_total = new
        series.eval_finished()

    Session.commit()


@register("remove", shorthelp="remove a season",
          dictionary=Commands_Season, sortorder=Commands_Season_Order)
@arguments(1, 2)
@selector
@interactive_selector
@paranoia(1)
def cm_season_remove(selector, seasonnum=None):
    """
    season remove [number]: [selector]
        Remove the season with number [number] from series
        matching [selector]. If [number] is not specified,
        remove the currently active season.
    """

    seasonnum = checkint(seasonnum, "season number")

    for series in selector.season_all():
        number = seasonnum or series.current

        # Delete
        query = (Season.query.filter(Season.series == series)
                             .filter(Season.num == number))

        if not query.all():
            print("Error: season number %d does not exist for series %s."
                   % (number, series.title))
        else:
            query.delete()

        # Set active
        if number == series.current:
            series.current = max(season.num for season in series.seasons
                                             if season.num != number)

        series.eval_finished()

    Session.commit()

@register("active", shorthelp="mark a different season as active",
          dictionary=Commands_Season, sortorder=Commands_Season_Order)
@arguments(1, 2)
@selector
@interactive_selector
@paranoia(2)
def cm_season_active(selector, seasonnum=None):
    """
    season active [number]: [selector]
        Mark the season with number [number] as the active
        season for all series matching [selector].

        If [number] is not specified, make the season with
        the highest number active.

        Relative numbers such as +2 or -1 may be used with
        [number].
    """

    if seasonnum is not None:
        if seasonnum[0] == '-':
            relative = True
            seasonnum = -checkint(seasonnum[1:], "season number")
        elif seasonnum[0] == "+":
            relative = True
            seasonnum = checkint(seasonnum[1:], "season number")
        else:
            relative = False
            seasonnum = checkint(seasonnum, "season number")

    for series in selector.season_all():
        if seasonnum == None:
            series.current = max(season.num for season in series.seasons
                                             if season.num != seasonnum)
        elif relative:
            series.current += seasonnum
        else:
            series.current = seasonnum

    Session.commit()
