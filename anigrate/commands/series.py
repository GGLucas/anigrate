import datetime

from anigrate.models import Session, Series, Season, Watched
from anigrate.util import (register, selector, selector_literal,
                   arguments, promptfor, debug, checkint, verbose,
                   paranoia, parseprogress, parsedate)

@register("add", shorthelp="add a new series")
@arguments(0, 6)
@selector_literal
def cm_add(name=None, category=None, progress=None, rating=None, duration=None, date=None):
    """
    add [category] [watched[/total][*seasons],..] [rating] [duration] [date]: [name]
        Add a new series entry with name specified by (name).
        Optionally, you can specify the category, duration, amount of episodes
        watched, amount of episodes total, amount of seasons and rating.

        If date is specified, any watch log entries created will have their watch
        dates set to this instead of the current date and time.
        See `help dates` for acceptable date formats.

        If no name is specified as selector, the add command will prompt for it 
        and any other arguments not specified either.
    """

    # Prompt for any missing arguments
    if not name:
        name = promptfor("Enter new series title")

        if not name:
            debug(" Error: Please input a series title.", False)

        if category is None:
            category = promptfor("Enter category", "")

        if progress is None:
            progress = promptfor("Enter series initial progress", "0/0")

        if rating is None:
            rating = promptfor("Enter series rating", "0")

        if duration is None:
            duration = promptfor("Enter episode duration in minutes", "24")

    # Check integer arguments
    if rating is not None:
        rating = checkint(rating, "rating")
    else:
        rating = 0

    if duration is not None:
        duration = checkint(duration, "duration")
    else:
        duration = 24

    if date is not None:
        date = parsedate(date)
    else:
        date = datetime.datetime.now()

    # Check category
    if category is None:
        category = ""

    # Parse progress argument
    seasons = parseprogress(progress)

    # Check if series exists
    if Series.exists(name, category):
        debug("Error: A series with this title already exists in this"
              " category.", False)

    # Create series
    series = Series(
        title=name,
        rating=rating,
        category=category,
        duration=duration,
    )

    series.ctime = series.mtime = date
    Session.add(series)

    # Create every season
    for num, (current, total) in enumerate(seasons):
        # Season entry
        season = Season(
            num=num+1,
            series=series,
            episode_total=total,
            current_watched=current,
        )

        Session.add(season)

        # Log entry
        if current > 0:
            watched = Watched(
                season=season,
                seasonnum=num+1,
                series=series,
                time=date,
                startep=0,
                finishep=current,
            )

            Session.add(watched)

    # Series info
    series.current = num+1
    series.eval_finished()

    Session.commit()

@register("category", shorthelp="set series category")
@arguments(1, 2)
@selector
@paranoia(2)
def cm_category(selector, value=None):
    """
    category [category]: (selector)
        Mark all series matched by (selector) as having category [category].
    """
    ## TODO: If selector is empty, show incremental switch

    for series in selector.all():
        orig = series.category

        # Prompt if not given
        if value is None:
            new = promptfor("Enter new category for series `%s`" % 
            series.title, orig, True)
        else:
            new = value

        if series.category != new and value is not None:
            verbose("Setting category to %s for %s..." % (new, series.title))

        series.category = new

    Session.commit()

@register("rate", shorthelp="set series rating")
@arguments(1, 2)
@selector
@paranoia(2)
def cm_rate(selector, value=None):
    """
    rate [score]: [selector]
        Rate all series matched by [selector] with [score].
    """
    ## TODO: If selector is empty, show incremental switch

    value = checkint(value, "rating")

    for series in selector.all():
        orig = series.rating

        # Prompt if not given
        if value is None:
            # Prompt
            new = promptfor("Enter new rating for series `%s`" % 
            series.title, orig)

            # Convert to number
            new = checkint(new, "rating", exit=False)
            if new == None: continue
        else:
            new = value

        if series.rating != new and value is not None:
            verbose("Setting rating to %d for %s..." % (new, series.title))

        series.rating = new

    Session.commit()

@register("duration", shorthelp="set series duration")
@arguments(1, 2)
@selector
@paranoia(2)
def cm_duration(selector, value=None):
    """
    duration [time]: [selector]
        Set the average duration of an episode in series matching [selector].
        This is used to calculate total watching time, defaults to 24 minutes
        per episode for every series.
    """
    ## TODO: If selector is empty, show incremental switch

    value = checkint(value, "duration")

    for series in selector.all():
        orig = series.duration

        # Prompt if not given
        if value is None:
            # Prompt
            new = promptfor("Enter new duration for series `%s`" % 
            series.title, orig)

            # Convert to number
            new = checkint(new, "duration", exit=False)
            continue
        else:
            new = value

        if series.duration != new and value is not None:
            verbose("Setting duration to %d for %s..." % (new, series.title))

        series.duration = new

    Session.commit()

@register("drop", shorthelp="mark a series as dropped")
@arguments(1)
@selector
@paranoia(2, verb="drop")
def cm_drop(selector):
    """
    drop: [selector]
        Mark all series matched by [selector] as dropped.
    """
    ## TODO: If selector is empty, show incremental switch

    for series in selector.all():
        if not series.dropped:
            verbose("Dropping %s..." % series.title)
        series.dropped = True

    Session.commit()

@register("undrop", shorthelp="mark a series as not dropped")
@arguments(1)
@selector
@paranoia(2, verb="undrop")
def cm_undrop(selector):
    """
    undrop: [selector]
        Mark all series matched by [selector] as not dropped.
    """
    ## TODO: If selector is empty, show incremental switch

    for series in selector.all():
        if series.dropped:
            verbose("Undropping %s..." % series.title)
        series.dropped = False

    Session.commit()

@register("length", shorthelp="set series length")
@arguments(1, 2)
@selector
@paranoia(2)
def cm_length(selector, value=None):
    """
    length [length]: (selector)
        Set the active season's length in episodes.
    """
    ## TODO: If selector is empty, show incremental switch

    value = checkint(value, "rating")

    for series in selector.all():
        orig = series.epstotal

        # Prompt if not given
        if value is None:
            # Prompt
            new = promptfor("Enter new length for series `%s`" % 
            series.title, orig)

            # Convert to number
            new = checkint(new, "length", exit=False)
            if new == None: continue
        else:
            new = value

        if series.rating != new and value is not None:
            verbose("Setting length to %d for %s..." % (new, series.title))

        series.epstotal = new
        series.current_season.episode_total = new

    Session.commit()

@register("remove", shorthelp="delete a series entry")
@arguments(1)
@selector
@paranoia(1, verb="remove", complete=True)
def cm_remove(selector):
    """
    remove: [selector]
        Completely remove any series that match [selector].
    """
    ## TODO: If selector is empty, show incremental switch

    for series in selector.all():
        # Delete series info
        Session.delete(series)

        # Delete watch log
        Watched.query.filter(
            Watched.series == series
        ).delete()

        # Delete seasons
        Season.query.filter(
            Season.series == series
        ).delete()

        verbose("Removing %s..." % series.title)

    Session.commit()
