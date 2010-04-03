from anigrate.models import Session
from anigrate.util import (register, arguments, selector, checkint,
                            verbose, promptfor,
                            paranoia, Commands_Season, 
                            Commands_Season_Order)

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
@paranoia(2)
def cm_season_add(selector, value=None, seasonnum=None):
    """

    """
    ## TODO: If selector is empty, show incremental switch
    pass


@register("length", shorthelp="set season length",
          dictionary=Commands_Season, sortorder=Commands_Season_Order)
@arguments(1, 3)
@selector
@paranoia(2)
def cm_season_length(selector, value=None, seasonnum=None):
    """
    season length [length] [season]: (selector)
        Set the length in episodes for season [season].

        If [season] is not given, set length for the active season.
    """
    ## TODO: If selector is empty, show incremental switch

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
            if new == None: continue
        else:
            new = value

        if series.rating != new and value is not None:
            verbose("Setting length to %d for season %d of %s..." % 
                      (new, seasonnum, series.title))

        series.epstotal = new
        series.season_bynum(seasonnum).episode_total = new

    Session.commit()
